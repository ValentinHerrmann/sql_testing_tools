SELECT Gemeinde.name
FROM Wanderweg_zu_Gemeinde,Gemeinde
WHERE Gemeinde.schluessel=Wanderweg_zu_Gemeinde.gemeindeschluessel
and (Gemeinde.regierungsbezirk="Oberbayern" or Gemeinde.regierungsbezirk="Niederbayern")