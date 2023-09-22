get_github_issues() {
  if [ $# -ne 2 ]; then
    echo "Usage: get_github_issues <username/repo> <access_token>"
    return 1
  fi

  local repo="$1"
  local access_token="$2"
  local api_url="https://api.github.com/repos/$repo/issues"

  # Make the API request using curl with authentication
  local response=$(curl -v -s -H "Authorization: token $access_token" "$api_url")

  # Check if the request was successful (HTTP status 200)
  #local status_code=$(echo "$response" | grep -o 'HTTP/1.1 [0-9]*' | awk '{print $2}')
  #if [ "$status_code" != "200" ]; then
  #  echo "Error: Failed to retrieve GitHub issues. HTTP status code $status_code"
  #  return 1
  #fi

  # Parse and display the list of issues
  echo "$response"
  #echo "$response" | jq -r '.[] | "Issue #" + (.number | tostring) + ": " + .title'
  #echo "$response" | jq -r '.[] | "Issue #" + (.number | tostring) + ": " + .title'

}

# Function to split a string into an array
split_string() {
    local input_string="$1"  # The input string to split
    local delimiter="$2"    # The delimiter to split the string by
    local -a result=()      # Declare an empty array to store the substrings

    IFS="$delimiter"       # Set the Internal Field Separator (IFS) to the delimiter
    read -ra result <<< "$input_string"  # Use 'read' to split the string into an array

    echo "${result[@]}"    # Print the array elements
}
# Function to write each element of an array to a file
write_array_to_file() {
    local array=("$@")    # Get all arguments as an array
    local output_file="$1"  # The name of the output file

    # Iterate through the array and write each element to the file
    for element in "${array[@]}"; do
        echo "$element" >> "$output_file"
        echo " "
    done
}
write_issues_to_file() {
    local array=("$@")    # Get all arguments as an array
    local output_file="issues.md"  # The name of the output file

    # Iterate through the array and write each element to the file
    echo "# GitHub Issues" > "$output_file"
    for element in "${array[@]}"; do
        echo "$element" >> "$output_file"
        echo " "
    done
}
# Example usage:
output_file="output.txt"
my_array=("Element 1" "Element 2" "Element 3")
write_array_to_file "$output_file" "${my_array[@]}"

# change to bin folder
cd ..
# open load variables
set -o allexport
source .env set
set +o allexport
echo "${GH_TOKEN}"
echo "${GH_USER}/${GH_PROJECT}"
echo "https://api.github.com/repos/${GH_USER}/${GH_PROJECT}/issues"
issues=$(get_github_issues "${GH_USER}/${GH_PROJECT}" "${GH_TOKEN}")
echo ${issues}
#echo $(write_issues_to_file "${issues[@]}")