rm -f linkccheckerrc

echo "[output]" > linkcheckerrc
echo "log=csv" >> linkcheckerrc
echo "fileoutput=csv" >> linkcheckerrc
echo "warnings=0" >> linkcheckerrc
echo "ignoreerrors=" >> linkcheckerrc
echo "  ^.* ^.*403.*" >> linkcheckerrc
echo "  ^.* ^.*418.*" >> linkcheckerrc
echo "  ^.* ^.*406.*" >> linkcheckerrc
echo "  ^.* ^.*503.*" >> linkcheckerrc
echo "" >> linkcheckerrc

echo "[csv]" >> linkcheckerrc
echo "filename=broken-links.csv" >> linkcheckerrc
echo "separator=|" >> linkcheckerrc
echo "parts=parentname,urlname,name,result" >> linkcheckerrc
echo "" >> linkcheckerrc

echo "[checking]" >> linkcheckerrc
echo "localwebroot=$(pwd)/site/public/" >> linkcheckerrc
echo "timeout=5" >> linkcheckerrc
echo "" >> linkcheckerrc

echo "[filtering]" >> linkcheckerrc
echo "ignore=" >> linkcheckerrc
echo "  ^.*doxygen-releases.*" >> linkcheckerrc
echo "  ^.*trac_archive.*" >> linkcheckerrc
echo "checkextern=1" >> linkcheckerrc
