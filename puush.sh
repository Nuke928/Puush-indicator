if [ -z "$1" ]
then
  echo "No API key"
  exit 1
elif [ -z "$2" ]
then
  echo "Specify a file to be uploaded"
  exit 2
elif ! [ -f "$2" -a -r "$2" ]
then
  echo "File '$2' is not valid (it is not a file or it is not readable)"
  exit 3
fi

curl "https://puush.me/api/up" -# -F "k=$1" -F "z=poop" -F "f=@$2"
