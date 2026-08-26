# Final Challenge Proposals for Compilation

This is the final side-by-side review. A blank **Proposed challenge text** cell means the pre-compilation wording should remain unchanged.

- Challenges reviewed: 99
- Proposed challenge-text changes: 17

| Lesson | Challenge | Pre-compilation challenge text | Proposed challenge text |
|---|---:|---|---|
| 01 - Hello Python! | 1 | Change the print() message to print(greeting, name, “!”). Assign (save with the = symbol) a new greeting in another language, like “Guten tag,”, to the variable greeting. | Store a greeting from another language, such as "Xin chao", in a variable called [greeting]. Change print() so it displays [greeting], then [name], then an exclamation mark. |
| 01 - Hello Python! | 2 | Change the program to ask for and output your friend’s name too. Change the message inside print() to also output “and” and your friend's name. | Ask for a friend's name and store it in a variable called [friend_name]. Change print() so it displays "Hello, [name] and [friend_name]!" using [name] and [friend_name]. |
| 01 - Hello Python! | 3 | Create a new program which asks the user what two subjects they study in school. Output a message to the user which tells them “I think subject1 and subject2 are great subjects!”. |  |
| 02 - Operators and Integers | 1 | Ask for two whole numbers, convert both with int(), and display their sum. |  |
| 02 - Operators and Integers | 2 | Store 2 as a non-zero secret number, divide the user's sum by it, and display the new total. |  |
| 02 - Operators and Integers | 3 | Create a program that asks for three whole numbers, subtracts the second and third from the first, and displays the total. |  |
| 03 - Decimal Numbers | 1 | Change the sample journey to 9 kilometres in 3 minutes. The labelled result should be 3.0 kilometres per minute. | Store [distance] / 2 in a variable called [halfway_distance]. Display [halfway_distance] before [speed]. Test 9 kilometres and 3 minutes; the halfway distance should be 4.5. |
| 03 - Decimal Numbers | 2 | Add a third decimal input called rest_minutes. Display total_minutes as travel minutes plus rest minutes. For 12.5 and 2.5, the total must be 15.0. |  |
| 03 - Decimal Numbers | 3 | Create a floor-area calculator. Ask for decimal length and width, multiply them, and display a labelled area. Test 4.5 by 2: the area should be 9.0. |  |
| 04 - Decisions | 1 | Run the starter once with "walk" and once with "read". Then replace only the walk recommendation with a library message. Both inputs must still lead to different messages. |  |
| 04 - Decisions | 2 | Personalise both routes: ask for the user's name, then include it in whichever recommendation appears. Check that the name is shown for both possible choices. |  |
| 04 - Decisions | 3 | A cafe asks, "Do you want tea?" Use if and else to build a two-way choice: yes displays "Tea is ready."; every other answer displays "Choose another drink." Test one input for each route. |  |
| 05 - More Decisions | 1 | A score of 9 should now count as Excellent. Adjust the first comparison, then prove the boundary by running scores 8 and 9 and recording the two different results. | Change the program so a score of 9 displays "Excellent". Test scores 8 and 9. |
| 05 - More Decisions | 2 | Add one elif branch so scores 3 and 4 display "Keep practising". Scores below 3 should display "Try again"; the Excellent and Good outcomes stay unchanged. |  |
| 05 - More Decisions | 3 | Create a temperature classifier with three outcomes: Hot at 30 or above, Warm from 20 to 29, and Cool below 20. Test 19, 20 and 30. |  |
| 06 - Logical Choices | 1 | Lower the age boundary to 14. Use the existing ticket rule, then test ages 13 and 14 with a ticket so the change is visible. | Change the age check from 12 to 14. Test ages 13 and 14 with a ticket. |
| 06 - Logical Choices | 2 | Add an adult exception with or: entry is allowed when the age-and-ticket rule is true or an adult is present. Test an under-age visitor with no ticket but with an adult. |  |
| 06 - Logical Choices | 3 | Build a club checker that asks whether the visitor is a member and has a valid pass. Use and so entry is allowed only when both answers are "yes"; otherwise show a refusal. Test one allowed and one refused route. |  |
| 07 - Nested Decisions | 1 | Change only the inner yes route so yes followed by yes displays "Wear a waterproof coat." | When it is raining, ask whether the wind is strong or light. Display "Wear a coat." for strong wind and "Take an umbrella." for light wind. Keep the dry-weather route unchanged. |
| 07 - Nested Decisions | 2 | Extend the dry-weather route. If raining is no, ask whether it is sunny; display "Take sunglasses." for yes and "No weather gear needed." for no. |  |
| 07 - Nested Decisions | 3 | Build a library-access checker. Ask whether the visitor has a card. Only card holders are asked whether a book is overdue. Display one clear message for all three possible routes. |  |
| 08 - Counted Loops | 1 | The display stops too soon. Change range() so the starter prints the first ten multiples, then check that the final line is the tenth multiple. |  |
| 08 - Counted Loops | 2 | Let the user choose where the table begins. Use range() with that starting multiplier to display five consecutive multiples. |  |
| 08 - Counted Loops | 3 | Create a three-line announcement. Ask for a short message, then use a for loop and range() to display "1 [message]", "2 [message]" and "3 [message]". Try it with "Ready". |  |
| 09 - Condition Loops | 1 | Choose a new target number. Keep the three-attempt limit, then guess it first and complete another run with three wrong guesses. Check that the program reports 1 try and 3 tries. | Change the program so the user has two attempts. Test one run by guessing 7 first and another with two wrong guesses. The program should display 1 try and 2 tries. |
| 09 - Condition Loops | 2 | Give the player five attempts. Update the finishing message to report the guesses used. Test an early correct guess and five unsuccessful guesses; both counts must be accurate. |  |
| 09 - Condition Loops | 3 | Create a door-code checker with a while loop that allows at most three attempts. Stop early when "open" is entered, then display either a success message or a final locked message with the attempts used. |  |
| 10 - Choosing Loop Structures | 1 | Make the counted warm-up display rounds 1 to 5. The condition-controlled section must still finish only when the user types done. |  |
| 10 - Choosing Loop Structures | 2 | Add an attempt counter to the while loop. After done is entered, display the number of answers entered. For wait, wait, done the count must be 3. |  |
| 10 - Choosing Loop Structures | 3 | Create a practice timer without real-time code. Use a for loop to display exactly four exercise stations, then a while loop to collect effort ratings until the user enters 0. Count and display the non-zero ratings. |  |
| 12 - Strings and Text | 1 | Make the greeting begin with "Welcome," and show the cleaned name. Try it with spaces and uneven capital letters in the input. |  |
| 12 - Strings and Text | 2 | A name badge needs a first name and surname. Extend the program so both answers are cleaned with strip() and title(), then display the finished full name. |  |
| 12 - Strings and Text | 3 | Choose a place you would like to visit. Build a destination label from a city and country, cleaning both answers before you display "Destination: [city] - [country]". |  |
| 13 - String Positions | 1 | Change the slice’s stop position so the preview contains four characters instead of three. Try "code" and "python"; both previews should contain four characters. |  |
| 13 - String Positions | 2 | Create a two-letter badge from two words. Use indexing to display the first character of each; use inputs with different capitalisation to inspect the result. |  |
| 13 - String Positions | 3 | Build a reference code for a six-letter word. Use two slices to display its first two characters, then characters five and six. Try "python": the two parts should be "py" and "on". |  |
| 14 - Changing Text Case | 1 | Make the displayed team name uppercase and the displayed code lowercase. Falcons and f7 should become FALCONS and f7. |  |
| 14 - Changing Text Case | 2 | Add a response input and store response.lower(). Display Accepted when the normalised response equals yes and Not accepted otherwise. |  |
| 14 - Changing Text Case | 3 | Build a badge formatter. Ask for a first name and a two-letter group code; display the name in lower case and the group code in upper case on separate labelled lines. |  |
| 15 - Joining Text | 1 | Use an underscore instead of a full stop. Asha and Khan should produce asha_khan. |  |
| 15 - Joining Text | 2 | Add a department input. Build account_label from lower-case last name, a hyphen and upper-case department. Khan and art should display khan-ART. |  |
| 15 - Joining Text | 3 | Create an event tag from a venue, an activity and a two-letter group. The visible tag must use the structure venue/activity-GROUP with the venue and activity in lower case. |  |
| 16 - Text Length and Lines | 1 | Change the heading to "Notice:" while keeping the message on the following line. Code now must still report 8 characters. | Remove spaces from the start and end of [message] before displaying and counting it. Test "Code now" with two spaces before and after it; the message should display as "Code now" and the count should be 8. |
| 16 - Text Length and Lines | 2 | Collect a title and a subtitle. Display both on separate lines, then display a labelled character count for each one. |  |
| 16 - Text Length and Lines | 3 | Create a two-line poster checker. Ask for a heading and one instruction, display the poster on two lines, and report the combined character count using the two len() results. |  |
| 17 - Lists | 1 | Prepare the starter for a weekend trip by replacing the initial list with three useful items. The user's extra item must still be appended and visible in the final list. |  |
| 17 - Lists | 2 | The user should add two items in total. Ask for a second item, append it, then show all four items in the final packing list. | Ask for a second item and append it to the list. Display all four items. |
| 17 - Lists | 3 | Make a movie-night checklist. Start with two items of your choice, ask the user for a third, append it, and display the finished list with a clear heading. |  |
| 18 - Random Whole Numbers | 1 | Turn the die into a twelve-sided die. Keep seed 7; the displayed result must stay between 1 and 12 inclusive. | Change the die so it can roll numbers from 1 to 12. Run the program several times; every result should be between 1 and 12. |
| 18 - Random Whole Numbers | 2 | Generate two six-sided rolls and display their total. With seed 7, the two stored rolls must be generated on separate lines. | Generate two six-sided rolls. Display both rolls and their total. |
| 18 - Random Whole Numbers | 3 | Create a random practice target. Ask for a minimum and maximum whole number, generate one target inside those inclusive bounds, and display it with a label. Test bounds 4 and 4; the target must be 4. |  |
| 19 - Random Steps and Choices | 1 | Generate a multiple of 5 from 5 through 30. Keep seed 4 and display the result as Move. | Generate and display a random multiple of 5 from 5 to 30. Run the program several times; every result should be a multiple of 5 in this range. |
| 19 - Random Steps and Choices | 2 | Add "green" to the colour choices and generate two independently stored colour selections. Display both selections on labelled lines. |  |
| 19 - Random Steps and Choices | 3 | Build a random training prompt. Choose an even repetition count from 2 through 12 and one activity from a three-item list you design. Display one instruction such as 8 jumps. |  |
| 20 - Reliable Menus | 1 | Change route 1 so it displays "Status ready." Invalid input and route 2 must keep their existing behaviour. |  |
| 20 - Reliable Menus | 2 | Add route 3 to display "Help: choose a number." Update the prompt and invalid guidance. Test the path 3, x, 2. |  |
| 20 - Reliable Menus | 3 | Build a repeating transport menu with two useful routes, one exit route and one invalid-input message. At least one useful route must ask a follow-up question and display a labelled response. |  |
| 21 - Character Codes | 1 | Display the previous letter by subtracting 1 from the character code. Input d must display c. |  |
| 21 - Character Codes | 2 | Ask for one lower-case letter a-w and a shift from 1 to 3. Add the shift to the character code and display the encoded letter. For c and 2, display e. |  |
| 21 - Character Codes | 3 | Create a three-character encoder without a loop. Ask for three lower-case letters a-y, move each code forward by 1, concatenate the three encoded characters, and display the encoded text. |  |
| 22 - List Positions and Updates | 1 | Replace the item at position 2 with scissors. The final list must display pencil, book and scissors in that order. |  |
| 22 - List Positions and Updates | 2 | After the replacement, ask for a second valid position and display the item currently stored there. For 1/folder then 1, the selected item must be folder. |  |
| 22 - List Positions and Updates | 3 | Build a three-stop route editor. Start with three place names, ask which valid position to change and the new place, then display the first stop and the complete updated route. |  |
| 23 - Inserting and Removing List Items | 1 | Insert "snack" at position 2 and keep the removal of coat. The final order must be water, snack, torch. |  |
| 23 - Inserting and Removing List Items | 2 | Ask for an item to insert at position 1, then ask for an existing item to remove. Display the list after each operation. Test map then coat. |  |
| 23 - Inserting and Removing List Items | 3 | Create a four-name running order editor. Insert a reserve at a user-chosen valid position, remove one known existing name by value, and display the final order one name per line using a for loop. |  |
| 24 - Deleting by List Position | 1 | Use position 0 as the completed task. The output must label email as completed and show the other three tasks in order. | Keep the user's deletion. Display the new first task with the label "Next:". Test position 0; "email" should be completed and "design" should be next. |
| 24 - Deleting by List Position | 2 | After the first deletion, ask for a second valid position in the shortened list, label that item, delete it, and display what remains. Test first 1 then 1. |  |
| 24 - Deleting by List Position | 3 | Build a queue editor with four names. Ask for one valid cancellation position, store and delete that name, then traverse the remaining queue with numbered positions using a counter. |  |
| 25 - Working Through Lists | 1 | Make each survey line read "Choice: [drink]" instead of "Drink: [drink]". The loop must still visit every item and the total must stay correct. |  |
| 25 - Working Through Lists | 2 | Add a fourth survey answer to the list. Before running, predict the last answer and the total that will appear; then check both. |  |
| 25 - Working Through Lists | 3 | Create a colour-survey summary with three answers of your choice. Use a for loop to label every colour, then use len() once to report how many answers were collected. |  |
| 26 - Building Lists with Loops | 1 | Collect exactly five notes instead of three. The program must display all five in their original input order. |  |
| 26 - Building Lists with Loops | 2 | Replace the fixed input loop with a condition-controlled loop. Keep asking for a note until stop is entered; do not append or display the sentinel stop. |  |
| 26 - Building Lists with Loops | 3 | Create a team roster builder. Ask how many names will be entered, collect exactly that many names into an empty list, then ask for one valid replacement position and update that name before displaying the final roster one name per line. |  |
| 28 - Reading 2D Lists | 1 | Select row 2. The output must identify Code and 15 from the same record. | Ask for a column from 0 to 1 as well as the row. Display the value in [clubs] at [row] and [column]. Test row 2 and column 0; the program should display "Selected field: Code". |
| 28 - Reading 2D Lists | 2 | Traverse every row and display each club name followed by its member count. Do not print the row brackets. |  |
| 28 - Reading 2D Lists | 3 | Create a three-row timetable. Each row stores a subject and room number. Ask for a valid row, then display a sentence containing both selected fields. Also display every subject name using a loop. |  |
| 29 - Updating 2D List Cells | 1 | Update row 2 to 17 members. The Code name and all other records must remain unchanged. | Change the second input so the user adds members instead of replacing the total. Test row 2 and add 2; "Code" should have 17 members and the other records should stay unchanged. |
| 29 - Updating 2D List Cells | 2 | Let the user choose a valid row and update both its club name and member count. Display the selected row before and after the two assignments. |  |
| 29 - Updating 2D List Cells | 3 | Create a three-row stock table containing item name and quantity. Ask for a valid row and a delivery amount, add that amount to the existing quantity, then display the updated record and every item quantity. |  |
| 30 - Changing 2D List Rows | 1 | Insert ["Drama", 11] at row position 0 and remove the deletion line. The final output must begin Drama 11. |  |
| 30 - Changing 2D List Rows | 2 | Ask for a new club name and member count, build a two-field row, append it, then ask for one valid row position to delete. Display the remaining rows. |  |
| 30 - Changing 2D List Rows | 3 | Build an event schedule editor with three [event, room] rows. Insert one user-created row at a valid position, delete a different valid row from the enlarged schedule, and display numbered remaining rows using a counter. |  |
| 31 - Searching 2D Lists | 1 | Change the target to Code. The program must display Members: 15 and must not display Club not found. | Change the search so the user enters a member count instead of a club name. Display the matching club. Test 15; the program should display "Club: code". |
| 31 - Searching 2D Lists | 2 | Extend the matching route to ask for a new member count and update the matched row. Display the updated record. Test Chess with 20 and Music. |  |
| 31 - Searching 2D Lists | 3 | Create a three-record book search with [title, pages] rows. Search case-insensitively by title, display the page count for a match, and display one not-found message only after every row has been checked. |  |
| 32 - Functions | 1 | Rewrite only the message inside show_greeting() so a caller sees "Hello, coder!" The function name and call stay unchanged. |  |
| 32 - Functions | 2 | A greeting is useful more than once. Add a second function call: call show_greeting() again so "Hello, Python learner!" appears twice. Predict the number of greetings before you run it. |  |
| 32 - Functions | 3 | Build one no-input function called show_tip() that displays a Python tip of your choice. Call it twice; the same tip should appear two times. |  |
| 33 - Functions with Results | 1 | Use the same function with two different pairs of scores. Before each run, work out the total you expect, then compare it with the returned value. |  |
| 33 - Functions with Results | 2 | Capture the returned total in a variable named score and display a labelled result on the next line. The function itself should not print the answer. |  |
| 33 - Functions with Results | 3 | A small shop needs a total_cost(price, delivery) function. Return the combined cost, store it, and display it with a clear label. For total_cost(12, 3), the result should be 15. |  |
| 34 - Several Functions | 1 | Change square() into triple(), update menu route 2, and make choice 2 with value 6 display Result: 18. |  |
| 34 - Several Functions | 2 | Add a third function called half(number) that returns number / 2. Add menu route 3 and an invalid-choice message. Test 3 with 5 and x with 5. |  |
| 34 - Several Functions | 3 | Build a measurement helper with separate functions to show a menu, calculate rectangle area, and calculate rectangle perimeter. The main program collects length and width, selects one calculation, and displays a labelled result; include an invalid route. |  |
| 35 - Functions with 2D Data | 1 | Change the search target to code. The final labelled result must be 15 while all three club names still display first. | Use find_members() to find the number of members in "art" and "code". Display "Art: 12" and "Code: 15" after the three club names. |
| 35 - Functions with 2D Data | 2 | Add a function total_members(records) that loops through the rows, maintains a running total, and returns it. Display the labelled total; the supplied data must produce 45. |  |
| 35 - Functions with 2D Data | 3 | Build a small results manager using [name, score] rows and three functions: display every record, search by lower-case name, and return the highest score. The main program must call all three and show a clear not-found message for a missing name. |  |
