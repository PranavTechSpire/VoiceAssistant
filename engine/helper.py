import re


def extract_yt_term(command):
    #Define a regular expression pattern to capture the song name
    # pattern = r'play\s+(.*?)\s+on|using\s+youtube'
    pattern = r'play\s+(.*?)\s+(?:on|using\s+youtube)'
    #USe re.search to find the match in thne command
    match = re.search(pattern, command, re.IGNORECASE)
    #If a match is found, return the extracted song name; otherwise , return none
    return match.group(1) if  match else None


#### 6. Make Helper Function to remove unwanted words from query
def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)
 
    return result_string


#### 7. Example of Helper Function
#Example usage
# input_string = "make a phone call to appa"
# words_to_remove = ['make', 'a', 'to', 'tu', 'phone', 'call', 'send', 'message', 'wahtsapp']

# result = remove_words(input_string, words_to_remove)
# print(result)
