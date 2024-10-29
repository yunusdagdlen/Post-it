#!/bin/bash

rm -rf ../static/app
mkdir -p ../static/app

rm -rf ../templates/app
mkdir -p ../templates/app

if [[ $OSTYPE == 'darwin'* ]]; then
  find ./dist -type f -name "*.js" -o -name "*.css" -exec sed -i '' -e 's/\/fonts\//\/static\/app\/fonts\//g' {} \;
  find ./dist -type f -name "*.js" -exec sed -i '' -e 's/\img\//static\/app\/img\//g' -e 's/\css\//static\/app\/css\//g' -e 's/\js\//static\/app\/js\//g'  {} \;
  find ./dist -type f -name "*.js" -exec sed -i '' -e 's/static\/app\/js\/v1\/vitally.js/js\/v1\/vitally.js/g' {} \;
  mv -f ./dist/css ./dist/fonts/ ./dist/js ../static/app/
  sed -i '' -e 's/href=\"\//href=\"\/static\/app\//g' ./dist/index.html
  sed -i '' -e 's/src=\"\//src=\"\/static\/app\//g' ./dist/index.html
  sed -i '' -e 's/FAVICON_PATH/\/static\/img\/favicon\/favicon.ico/g' ./dist/index.html

elif [[ $OSTYPE == 'linux'* ]]; then
  find ./dist -type f -name "*.css" -exec sed -i 's/\/fonts\//\/static\/app\/fonts\//g' {} \;
  find ./dist -type f -name "*.js"  -exec sed -i 's/\/fonts\//\/static\/app\/fonts\//g' {} \;
  find ./dist -type f -name "*.js" -exec sed -i 's/\img\//static\/app\/img\//g' {} \;
  find ./dist -type f -name "*.js" -exec sed -i 's/\css\//static\/app\/css\//g' {} \;
  find ./dist -type f -name "*.js" -exec sed -i 's/css\//static\/app\/css\//g' {} \;
  find ./dist -type f -name "*.js" -exec sed -i 's/\js\//static\/app\/js\//g'  {} \;
  find ./dist -type f -name "*.js" -exec sed -i 's/static\/app\/js\/v1\/vitally.js/js\/v1\/vitally.js/g'  {} \;
  mv -f ./dist/css ./dist/fonts/ ./dist/js ../static/app/
  sed -i 's/href=\"\//href=\"\/static\/app\//g' ./dist/index.html
  sed -i 's/src=\"\//src=\"\/static\/app\//g' ./dist/index.html
  sed -i 's/FAVICON_PATH/\/static\/img\/favicon\/favicon.ico/g' ./dist/index.html
else
  echo "Unsupported Operating System"
  exit 2
fi
mv -f ./dist/index.html ../templates/app/

rm -rf ./dist

echo "OK"