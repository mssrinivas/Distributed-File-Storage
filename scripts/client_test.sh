base_dir=$(dirname "$0")/..

cd "${base_dir}"

for i in {0..1}
do
  cp "./data/test_in.txt" "./data/test_in.txt_copy_$i"
  echo "Running job: $i"
#  for j in {1..20};do cat "./data/test_in.txt" >> "./data/test_in.txt_copy_$i"; done
  python3 ./src/SendDataExample.py "./data/test_in.txt_copy_$i"
  rm "./data/test_in.txt_copy_$i"
done

#python3 ./src/SenderNode.py "./data/big_file.data"