#!/bin/bash
function replaceLineInFile() {
  if [ $# -ne 3 ]; then
    echo "Usage: replaceLineInFile <filename> <target_line> <replacement_line>"
    return 1
  fi

  local filename="$1"
  local target_line="$2"
  local replacement_line="$3"

  if [ ! -f "$filename" ]; then
    echo "File '$filename' not found."
    return 1
  fi
  local line=""
  local backup="$filename.bak"
  echo "# start" > temp.env
  while IFS= read -r line; do
    # Process each line here, you can replace this with your own logic.
    #echo "Line: $line"
    if [ $line = $target_line ]; then
      echo $replacement_line >> temp.env
    else
      echo "$line" >> temp.env
    fi

  done < "$filename"
  cp "temp.env" "$filename"
}

#readLinesFromFile
echo "GH_BRANCH=GH_BRANCH" > workout.env
echo "GH_BRANCH2=GH_BRANCH" >> workout.env
echo "GH_BRANCH3=GH_BRANCH" >> workout.env

echo $(replaceLineInFile "workout.env" "GH_BRANCH=GH_BRANCH" "GH_BRANCH=GH_xx")
