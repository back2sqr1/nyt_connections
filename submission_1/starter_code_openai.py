import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client

client = openai.OpenAI(
    api_key="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"
)
# Initialize Claude client


def format_words(words):
    """Format the 16 words into a clean string"""
    return ", ".join(words)


def get_connections_solution(words, previous_attempts=None, remaining_words=None, isOneAway = False, correctGroups =None, strikes = 0):
    """Ask Claude to solve the Connections puzzle using structured reasoning"""

    prompt = f"""
    
Here are the remaining words {words}
You are solving a NYT Connections puzzle. The goal is to group 16 words into 4 sets of 4 words each. Here are examples of actual puzzle solutions to learn from:

Example 1:
Words: HEDGE, SEE-SAW, WAVER, YO-YO, BINGO, MARCO POLO, TAG, UNO, COMMUTE, MEDICINE, PROMPTER, VISION, BACON, CLOSE, MUNCH, WHISTLER
Solution: 
- Group 1: HEDGE, SEE-SAW, WAVER, YO-YO ("Wavering, EQUIVOCATE")
- Group 2: BINGO, MARCO POLO, TAG, UNO (Games where you say the game's name)
- Group 3: COMMUTE, MEDICINE, PROMPTER, VISION (Words that can start with TELE_)
- Group 4: BACON, CLOSE, MUNCH, WHISTLER (PAINTERS (references and history))

Example 2:
Words: DOLLY, ROLLERBLADE, SKATEBOARD, WAGON, BOOM, RISE, SPIKE, SURGE, BEST BOY, IDEA, KRONER, STABLES, DUCT, ELECTRICAL, GAFFER, PACKING
Solution: 
- Group 1: DOLLY, ROLLERBLADE, SKATEBOARD, WAGON ("Things with Wheels")
- Group 2: BOOM, RISE, SPIKE, SURGE (Upswings)
- Group 3: DUCT, ELECTRICAL, GAFFER, PACKING (Kinds of Tape)
- Group 4: BEST BOY, IDEA, KRONER, STABLES (RETAIL CHAINS WITH A LETTER CHANGED)


Learn from these patterns:
1. Words often have multiple meanings - look for the less obvious one
2. Some words are deliberately misleading (like HAND in Example 2)
3. Categories are usually clear once found - not overly complex
4. The difficulty levels (yellow/green/blue/purple) correlate with how obvious the grouping is

Now, analyze the current puzzle systematically:

1. Initial Analysis:
   - List each word and note its primary meaning
   - Note any secondary meanings or common usages
   - Identify if it's commonly part of phrases/idioms
   - Check if it can be part of compound words

2. Pattern Recognition (in order of priority):

  a) Word Relationships:
      - Words that can combine with a common word
      - Words that follow a shared pattern
      - Words that fit "_____ X" or "X _____" format
      - Common phrases "Silly Goose" 
      - Famous brands "Dove Soap, Tide pods"
    b) Abstract Connections:
      - Thematic relationships
      - Metaphorical associations
      - Cultural references
   c) Direct Categories:
      - Common taxonomies (animals, colors, etc.)
      - Functional groups (tools, vehicles, etc.)


3. Systematic Verification:
   For each potential group:
   a) Test if EXACTLY 4 words fit the pattern
   b) Verify no other words could fit
   c) Confirm the connection is equally strong for all 4
   d) Check if words might work better in other groups

4. Connection Types to Consider:
   a) Semantic Connections:
      - Direct synonyms/antonyms
      - Words in the same category
      - Words with similar connotations

   b) Structural Connections:
      - Common prefixes/suffixes
      - Rhyming patterns
      - Letter patterns
      - language homophones (ex. bask, check, finish, tie)

   c) Contextual Connections:
      - Words used in similar situations
      - Words from common expressions
      - Words related to specific domains
      - Words related to trends (ex. Boa, Corset, Fan, Gloves, for Burlesque Wear)
      - Common sayings like (Good, Penny, Please, Woman, for words after (PRETTY _ )
      - Words related to pop culture (Bad, Beach, Hardy, Pet Shop, (words that can have boys appended to them), like the beach boys or the bad boys)

5. Common Patterns:
   - Words that can all precede/follow another word
   - Parts of common phrases
   - Items in a set/collection
   - Words with similar function/purpose

Provide the one group you are most sure of
as your final answer. I will enter this into
the puzzle and give you feedback: I will tell
you whether it is correct, incorrect, or nearly
correct (3/4 words).
Then we will continue until the puzzled is
solved, or you lose.

Here are the remaining words to group: {format_words(remaining_words)}
DON'T MAKE UP WORDS! YOU MUST USE THESE WORDS

The goal is to find ONE group of 4 words that share a common theme. Be very careful about these common tricks:

1. Words might have multiple meanings (e.g., "SPRING" could be a season, a coil, or to jump)
2. Words might be part of common phrases (e.g., "HEART" could group with other card suits)
3. Words might combine with a hidden word (e.g., "FIRE" + [WORK, PLACE, FIGHTER, FLY])
4. Words might be used as different parts of speech (e.g., "LIGHT" as noun/verb/adjective)
5. Look for patterns in word structure, not just meaning
6. Consider less obvious categories (e.g., words that can follow/precede another word)
7. Watch for themed puzzles (holidays, current events)
8. Keep in mind that these aren't that complicated, usually can be done by the average person
9. Word associations must be equally strong for all the words in the guess
10. Popular references will be frequently used, so don't be afraid to link ideas

WORK TOWARDS the distinctive words first, they often are easier to dissociate from the others
Here's an example
Example 3:
Words: DESIRE, LONG, PINE, YEN, FORTUNE, MAD, NATURE, O, BOND, M, MONEYPENNY, Q, BUBBLEGUM, EURO, K, POWER
Solution: 
- Group 1: DESIRE, LONG, PING, YEN (Theme: Yearn, Note: YEN and EURO will easily mix up as money)
- Group 2: FORTUNE, MAD, NATURE, O (Theme: Magazines, Note: O, M, Q, K easily mix up as letters)
- Group 3: BOND, M, MONEYPENNY, Q (Theme: Characters in Bond Movies)
- Group 4: BUBBLEGUM, EURO, K, POWER (Theme: Words that precede "pop" in music genres)
If a group is too easy, be cautious of selecting it


If the group only strongly fits with two or three, it is probably not a correct group

Its important that these categories only have 4 words associated with them. Each guess should be checked to make sure only 
4 words match that category.

Don't use previous attempts!!! 
Do not use previous attempts even if the themes are different, no same groups

Here are the previous attempts, you cannot pick any of the previous groups {previous_attempts}

Wrong answers should be completely avoided, so try a different theme.
If its close, try switching a word out within the similar theme.

If any of the attempts were wrong, don't even go close to them
"""
    prompt += """
Please analyze these words and provide just ONE group of 4 related words:


Verify:
1. The theme is equally strong for all 4 words
2. No other remaining words could fit this theme
3. Do not make up words that aren't in the words list

Do not add ' marks in the 4 words
words should be in one line, explanation in a different line
Format your response like this:
[4 words] ex. [POWER, ROOT, EXPONENT, RADICAL]
"""

    messages = [
        {"role": "system", "content": """You are an expert NYT Connections puzzle solver with a perfect track record. You understand that these puzzles are designed to be solvable by average players and follow consistent patterns. You avoid overly complex or obscure connections. You're especially good at:
1. Identifying misleading words with multiple meanings
2. Finding hidden patterns that become obvious once revealed
3. Recognizing common puzzle construction patterns
4. Verifying that groups contain exactly 4 words with equally strong connections
5. Ensuring no other words could fit the proposed grouping
6. Learning from previous puzzle solutions to recognize common patterns
7. Go for the most distinctive words first
8. DO NOT REPEAT groups
9. Prioritize close calls
10. Do not go for easy answers like (THE WORD ENDS with O)"""},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0,  # We want consistent, logical answers
        max_tokens=2000
    )

    return response.choices[0].message.content


def extract_words_from_response(response):
    """Extract the 4 words from Claude's formatted response"""
    words = []
    lines = response.split('\n')

    # Try multiple patterns to find the words
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            continue

        # Look for lines with exactly 4 comma-separated words
        if ',' in line:
            # Clean up the line
            clean_line = line.replace('[', '').replace(']', '').strip()
            word_list = [w.strip().lower() for w in clean_line.split(',')]
            word_list = [w for w in word_list if w]  # Remove empty strings

            if len(word_list) == 4:
                # Verify these are actual words from the puzzle
                if all(len(w) > 0 for w in word_list):
                    return word_list

        # Also look for lines after "Group (COLOR):"
        if 'Group' in line and '(' in line and ')' in line:
            # Check next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].replace('[', '').replace(']', '').strip()
                word_list = [w.strip().lower() for w in next_line.split(',')]
                word_list = [w for w in word_list if w]
                if len(word_list) == 4:
                    return word_list

    return []  # Return empty list if no valid group found


def model(words, strikes, isOneAway, correctGroups, previousGuesses, error):
    """
    _______________________________________________________
    Parameters:
    words - 1D Array with 16 shuffled words
    strikes - Integer with number of strikes
    isOneAway - Boolean if your previous guess is one word away from the correct answer
    correctGroups - 2D Array with groups previously guessed correctly
    previousGuesses - 2D Array with previous guesses
    error - String with error message (0 if no error)

    Returns:
    guess - 1D Array with 4 words
    endTurn - Boolean if you want to end the puzzle
    _______________________________________________________
    """

    # Your Code here
    # Good Luck!

    # Example code where guess is hard-coded
    guess = ["apples", "bananas", "oranges", "grapes"]  # 1D Array with 4 elements containing guess
    endTurn = False  # True if you want to end puzzle and skip to the next one

    previous_attempts = previousGuesses.copy()

    wrong_guesses = 0
    solution = get_connections_solution(words, previous_attempts, words, isOneAway, correctGroups, strikes)

    print("SOLUTION", solution, words)
    # Extract the words from Claude's response
    proposed_words = extract_words_from_response(solution)
    for i in range(len(proposed_words)):
        proposed_words[i] = proposed_words[i].upper()
        if proposed_words[i][0] == "'":
            proposed_words[i] = proposed_words[i][1:-1]
    print("\nProposed words:", ", ".join(proposed_words))
    # Get the incorrect word

    return proposed_words, endTurn
