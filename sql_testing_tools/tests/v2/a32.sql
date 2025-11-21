SELECT Gemeinde.name
FROM Wanderweg, Gemeinde
WHERE Wanderweg.schluessel=Wanderweg_zu_Gemeinde.gemeindeschluessel and Gemeinde.regierungsbezirk ("Oberbayern" or "Niederbayern")