rm broken-links.md
cp broken-links.csv broken-links.md
sed -i 's/\(.*\)/|\1|/' broken-links.md
sed -i '1i # Broken Links' broken-links.md
sed -i '3i |-|-|-|' broken-links.md