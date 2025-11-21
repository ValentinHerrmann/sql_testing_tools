SELECT  gemeinde.name
FROM Gemeinde, WAnderweg_zu_Gemeinde
WHERE (regierungsbezirk = "Oberbayern" OR regierungsbezirk = "Niederbayern") AND wanderweg_zu_Gemeinde.gemeindeschluessel = Gemeinde.schluessel