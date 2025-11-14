SELECT  gemeinde.name
FROM Gemeinde, WAnderweg_zu_Gemeinde
WHERE (kreis = "OBERBAYERN" OR Kreis = "Niederbayern") AND wanderweg_zu_Gemeinde.gemeindeschluessel = Gemeinde.schluessel