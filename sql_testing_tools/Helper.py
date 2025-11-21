try:
    import BaseAccess as Ba
    import TokenProcessing as Tp
except ImportError:
    from . import BaseAccess as Ba
    from . import TokenProcessing as Tp

import requests
import sqlparse

from sqlparse.sql import Identifier, IdentifierList, Where, Comparison, Function, Parenthesis
from sqlparse.tokens import Keyword, DML, Name, Wildcard


sql = ""
sol = ""
bd = None
kw_sel = 'SELECT'
kw_frm = 'FROM'
kw_by = ' BY'
kw_grp = 'GROUP' + kw_by
kw_ord = 'ORDER' + kw_by
kw_whr = 'WHERE'
kw_lim = 'LIMIT'
kw_hav = 'HAVING'
semcol = ';'



def setup(sql_path,sol_path):
    global sql, sol, bd    
    if(bd == None):
        bd = Ba.getTableDict()
    if(sql_path and sql_path != ""):
        sql = normalizeSQLQuery(Ba.getSQLFromFile(sql_path), bd)
    if(sol_path and sol_path != ""):
        sol = normalizeSQLQuery(Ba.getSQLFromFile(sol_path), bd)
    if(sql=='' or sol==''):
        raise AssertionError("\n\nSQL-Datei ist leer. Aufgabe wurde noch nicht bearbeitet.")
    

def normalizeSQLQuery(query, base_dict):
    try:
        query = query.replace("\"", "'").replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ").strip()
        parsed = sqlparse.parse(query)[0]
        parsed.tokens = [token for token in parsed.tokens if not token.is_whitespace]
    except Exception as e:
        raise AssertionError(f"\nFehler beim Parsen der SQL-Abfrage: {str(e)}")

    formatted_query = []
    alias_map = {}

    # First pass to process FROM clause and populate alias_map
    for token in parsed.tokens:
        if token.is_whitespace:
            continue
        elif token.ttype is Keyword and token.value.upper() == kw_frm:
            formatted_query.append(kw_frm)
        elif isinstance(token, Identifier) and formatted_query and formatted_query[-1] == kw_frm:
            il = IdentifierList([token])
            formatted_query.append(Tp._from(il, alias_map, base_dict))
            Tp._from(il, alias_map, base_dict)
        elif isinstance(token, IdentifierList) and formatted_query and formatted_query[-1] == kw_frm:
            formatted_query.append(Tp._from(token, alias_map, base_dict))
            Tp._from(token, alias_map, base_dict)

    formatted_query = []

    # Second pass to process SELECT, WHERE, GROUP BY, ORDER BY, and LIMIT clauses
    for token in parsed.tokens:
        if token.is_whitespace:
            continue
        elif token.ttype is DML and token.value.upper() == kw_sel:
            formatted_query.append(kw_sel)
        elif token.ttype is Keyword and token.value.upper() == kw_frm:
            formatted_query.append(kw_frm)  
        elif token.ttype is Keyword and token.value.upper() == kw_grp:
            formatted_query.append(kw_grp)
        elif token.ttype is Keyword and token.value.upper() == kw_ord:
            formatted_query.append(kw_ord)
        elif token.ttype is Keyword and token.value.upper() == kw_lim:
            formatted_query.append(kw_lim)
        elif (isinstance(token, IdentifierList) or isinstance(token, Identifier)) and formatted_query and formatted_query[-1] == kw_frm:
            formatted_query.append(Tp._from(token, alias_map, base_dict))
        elif (isinstance(token, IdentifierList) or isinstance(token, Identifier)) and formatted_query and formatted_query[-1] == kw_grp:
            formatted_query.append(Tp._groupby(token, alias_map, base_dict))
        elif (isinstance(token, IdentifierList) or isinstance(token, Identifier)) and formatted_query and formatted_query[-1] == kw_ord:
            formatted_query.append(Tp._orderby(token, alias_map, base_dict))
        elif isinstance(token, Where):
            formatted_query.append(kw_whr)
            formatted_query.append(Tp._where(token, alias_map, base_dict))
        elif formatted_query and formatted_query[-1] == kw_sel and (isinstance(token, IdentifierList) or isinstance(token, Function) or isinstance(token, Identifier)):
            if isinstance(token, Function):
                token = IdentifierList([token])
            formatted_query.append(Tp._select(token, alias_map, base_dict))
        elif formatted_query and formatted_query[-1] == kw_lim:
            formatted_query.append(Tp._limit(token))
        else:
            formatted_query.append(str(token))

    return " ".join(formatted_query)

def find_table_for_column(data_dict, target_value, relevant_tables):
    l = []
    for key, value_list in data_dict.items():
        if key.lower() in relevant_tables:
            for sublist in value_list:
                if sublist and sublist[0].lower() == target_value.lower():
                    l.append(key)
    if len(l) == 0:
        for key, value_list in data_dict.items():
            for sublist in value_list:
                if sublist and sublist[0].lower() == target_value.lower():
                    l.append(key)
    return l

def getTableScheme(table_name: str, table_dict: dict):
    tab = table_dict[table_name]

    # Format the schema
    schema = "(" + ",".join([f"{col[0]}:{col[1]}" for col in tab]) + ")"
    return schema

def getCosetteKeyFromFile():
    try:
        with open("cosette_apikey.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "NOKEY"

def buildAndSendCosetteRequest(base_dict, sql, sol):

    err = ""
    for _ in range(2):
        try:
            api_key=getCosetteKeyFromFile()


            schema = ""
            for tab in base_dict.keys():
                schema += f"schema sch{tab}{getTableScheme(tab, base_dict)};\n"
            for tab in base_dict.keys():
                schema += f"table {tab}(sch{tab});\n"

            q1 = "query q1\n`"+sql+"`;\n"
            q2 = "query q2\n`"+sol+"`;\n"

            cosette = "-- random Kommentar\n" + schema + q1 + q2 + "verify q1 q2;\n"
            print(cosette)

            r = requests.post("https://demo.cosette.cs.washington.edu/solve",data={"api_key": api_key, "query": cosette}, verify=False)

            print(r.text)
            return (r.json()['result'],r.text)
        except Exception as e:
            err = str(e)
    return ("ERR", err)


def check_keywords(start_word:str, end_words:list):
    start_word = start_word.lower()

    if(start_word not in sol.lower() and start_word not in sql.lower()):
        return ""

    if(start_word in sql.lower()):
        start = sql.lower().find(start_word) + len(start_word)
        end = -1
        for kw in end_words:
            index = sql.lower().find(kw.lower(), start)
            if -1 < index < end or end == -1:
                end = index
        if(end == -1):
            end = len(sql)

        submission = str.strip(sql[start:end])

        start = sol.lower().find(start_word) + len(start_word)
        end = -1
        
        for kw in end_words:
            index = sol.lower().find(kw.lower(), start)
            if -1 < index < end or end == -1:
                end = index
        if(end == -1):
            end = len(sol)

        solution = str.strip(sol[start:end])

        if submission == solution:
            return ""
    return "Der '"+start_word+"' Teil der SQL-Abfrage ist nicht korrekt (oder nicht automatisch überprüfbar)."


def checkColumns(sql_path="", sol_path=""):
    setup(sql_path, sol_path)
    return check_keywords(kw_sel+" ", [kw_frm, kw_whr, kw_grp, kw_ord, kw_lim, semcol, kw_hav])


def checkTables(sql_path="", sol_path=""):
    setup(sql_path, sol_path)
    return check_keywords(kw_frm+" ", [kw_sel, kw_whr, kw_grp, kw_ord, kw_lim, semcol, kw_hav])


def checkCondition(sql_path="", sol_path=""):
    setup(sql_path, sol_path)
    return check_keywords(kw_whr+" ", [kw_sel, kw_frm, kw_grp, kw_ord, kw_lim, semcol, kw_hav])


def checkOrder(sql_path="", sol_path=""):
    setup(sql_path, sol_path)
    return check_keywords(kw_ord+" ", [kw_sel, kw_whr, kw_grp, kw_frm, kw_lim, semcol, kw_hav])


def checkGroup(sql_path="", sol_path=""):
    setup(sql_path, sol_path)
    return check_keywords(kw_grp+" ", [kw_sel, kw_whr, kw_grp, kw_ord, kw_lim, semcol, kw_hav])


def checkEquality(sql_path="", sol_path=""):
    setup(sql_path, sol_path)

    if sql == sol:
        return ""
    
    
    sql_build_fail = ""
    sol_build_fail = ""
    try:
        Ba.runAndGetStringTable_fromFile(sql_path)
    except Exception as e:
        sql_build_fail = str(e)
    try:
        Ba.runAndGetStringTable_fromFile(sol_path)
    except Exception as e:
        sol_build_fail = str(e)
        
    if(sql_build_fail != "" or sol_build_fail != ""):
        return "\n\nFehler beim Ausführen der Abfrage. Vermutlich enthält die Abfrage Syntaxfehler:\n" + sql_build_fail + "\n" + sol_build_fail

    result = buildAndSendCosetteRequest(bd, sql, sol)

    if result[0] == "ERR":
        return "\n\nFehler bei der automatischen Überprüfung der Abgabe. Es kann keine Aussage über die Korrektheit der Abgabe getroffen werden."
    elif result[0] != "EQ":
        return "\n\nDie Abgabe stimmt nicht mit der Musterlösung überein."
    return ""


