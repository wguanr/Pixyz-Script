filteredOccurrencesA = scene.getFilteredOccurrences("(Property(\"Name\").Matches(\"^.*Fram.*$\") OR (Property(\"Name\").Matches(\"^.*Rail.*$\") OR (Property(\"Name\").Matches(\"^.*内.*$\") OR (Property(\"Name\").Matches(\"^.*Door.*$\") OR (Property(\"Name\").Matches(\"^.*Plumbing.*$\") OR (Property(\"Name\").Matches(\"^.*MEP.*$\") OR (Property(\"Name\").Matches(\"^.*Park.*$\") OR (Property(\"Name\").Matches(\"^.*Equipment.*$\") OR (Property(\"Name\").Matches(\"^.*Furniture.*$\") OR (Property(\"Name\").Matches(\"^.*隔.*$\") OR Property(\"Name\").Matches(\"^.*Generic.*$\")))))))))))")  
filteredOccurrencesS = scene.getFilteredOccurrences("(Property(\"Name\").Matches(\"^.*Fram.*$\") OR Property(\"Name\").Matches(\"^.*Rail.*$\")OR Property(\"Name\").Matches(\"^.*Pipe.*$\")OR Property(\"Name\").Matches(\"^Generic.*$\"))))")

filteredOccurrences = scene.getFilteredOccurrences("Property(\"Name\").Matches(\"^.*dwg$\")")
scene.deleteOccurrences(filteredOccurrences)