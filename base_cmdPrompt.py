'''
Base File for sorting and
organizing movie list
so as to not have to do it on
paper

@Author: Zachary Kirby
@Date: 4-29-16


to add: new-- edit, delete
'''
import sqlite3
import time, math

INTRO = '''Welcome to the interactive movie catalog!
type in a movie name to search a movie or type 'help' to see a list of other commands'''

HELP_PRESETS = '''\n\nList of Commands: \n>> Help \n>> Search \n>> New \n>> Sort \n
type the name of a command to see more on the command.
To see more on a subset command type as such: BaseCommand(subset)\n'''

SEARCH_PRESETS = '''\n\nType a movie name (spelled correctly) to find all the info on that movie\n
Other commands available in search: ratings, movies. \nTo use a command type the command and then the movie name'''

NEW_PRESETS = '''\n\nTo add a movie type 'add' and then enter the information as instructed'''

SORT_PRESETS = '''\n\nUse this command to view the movies in a sorted fashion\nCommands available: by category, by rank, suggest [movie], rating [rating value]'''

STATISTICS_PRESETS = '''\n\nThis Command prompt allows you to run various statistics on several of the variables in the database\nCommands available: average'''

def process(command):
    '''processes commands prevents
     fractures within main loop'''
    global command_repository, global_cmd_word
    call = command.lower()
    presets = {'help': HELP_PRESETS, 'search': SEARCH_PRESETS, 'new':NEW_PRESETS, 'sort':SORT_PRESETS, 'stats':STATISTICS_PRESETS}
    try:
        print(presets[call])
        global_cmd_word = call
    except Exception as e:
        print("System Failed to Process Command: "+str(e))

def helpf():
    '''help commands prompt
     see extra help on commands'''
    global input_list, command_repository
    info = {'help':'This prompt lets you learn more about the other commands in the system\nOther commands in help specific environment: history',
            'search':'This prompt lets you research and view the various movies in the system',
            'new':'This prompt lets you add a new movie to the system',
            'search(rating)':'lets you see just the rating of a movie, type "all" to see rating statistics\n--For ordered ratings use tac o (-o or -O)\n--For personal ratings use tac p (-p or -P)',
            'new(add)':'Lets you add a movie to the data base',
            'search(movies)':'Displays all the movies in the data base',
            'help(history)':'Displays recent history of what has been selected',
            'sort':'This prompt lets you view the movies in a sorted, strastisifed fashion',
            'new(delete)':'delete a movie in the repository',
            'stats':'This prompt lets you run various statistics on the movie repository'}
    try:
        command = (input_list[-1]).lower()
        if command in info:
            print("\nInformation on {}: \n{}\n".format(command, info[command]))
        elif command == 'history':
            for i, hist in enumerate(input_list):
                print(str(i)+". "+hist)
        else:
            print("Couldn't find information on that command")
    except Exception as e:
        print("Error at processing 'help' command: "+str(e))

def new():
    '''add movies and edit
    existing entries in the DB'''
    global c, input_list, conn

    extra_commands = ['add', 'edit', 'delete', 'add watch', 'remove watch']
    try:
        command = (input_list[-1]).lower()

        if command == extra_commands[0]:
            name = str(input("\n   Movie Name: "))
            rating = int(input("   Rating: "))
            personal = int(input("   Personal Rating: "))
            tag = str(input("   Tags: "))
            category = str(input("   Category: "))
            c.execute("INSERT INTO movieDataBase (name, rating, personal, tag, category) VALUES (?, ?, ?, ?, ?)",
            (name, rating, personal, tag, category))
            conn.commit()
            print("Processing...");time.sleep(1.5);print("Finished\n")
        elif command == extra_commands[1]:
            print("\nUpdate a movie, can change: rating, personal rating, tags, category.")
            movie_selected = input("   Name: ")
            update = input("   What do you want to update: ")
            new_value = str(input("   New value: "))
            update_string = "UPDATE movieDataBase SET {} = '{}' WHERE name = '{}'".format(update, new_value, movie_selected)
            c.execute(update_string)
            conn.commit()
            print("Processing...");time.sleep(1.5);print("Finished\n")
        elif command == extra_commands[2]:
            print("\nDelete Movie or Documentary")
            to_delete = input("   Name: ")
            double_check = input("   Are you sure: (y or n)")
            if double_check == ('y' or 'Y'):
                c.execute(delete_string)
                conn.commit()
                print("Processing...");time.sleep(1.5);print("Finished\n")
            else:
                print("Deleted not Processed")
        elif command == extra_commands[3]:
            print("\nAdd a Movie to the Watch List")
            name = str(input("Movie Name: "));rating = 0; personal = 0; tag = ""; category = "wli"
            c.execute("INSERT INTO movieDataBase (name, rating, personal, tag, category) VALUES (?, ?, ?, ?, ?)",
            (name, rating, personal, tag, category))
            conn.commit()
            print("Processing...");time.sleep(1.5);print("Finished\n")
        elif command == extra_commands[4]:
            print("\nWhich movie to move off watch list: ")
            name = str(input("\n   Movie Name: "))
            rating = int(input("   Rating: "))
            personal = int(input("   Personal Rating: "))
            tag = str(input("   Tags: "))
            category = str(input("   Category: "))
            c.execute()
        else:
            print("Im sorry that command is not accessible in this command mode")
    except Exception as e:
        print("Error at new: "+str(e))

def sort():
    '''sort the different movie selections into
    different columns by characteristic'''
    global c, input_list

    extra_commands = ['by category', 'by rank', 'suggest','rating']

    try:
        command = (input_list[-1])

        if command.startswith(extra_commands[0]):
            print("\nList of Movies: ")
            c.execute("SELECT name FROM movieDataBase WHERE category = 'Movie'");data = c.fetchall()
            for i,row in enumerate(data):
                print(str(i+1)+") "+row[0])
            print("\nList of Documentaries: ")
            c.execute("SELECT name FROM movieDataBase WHERE category = 'Documentary'");data = c.fetchall()
            for i,row in enumerate(data):
                print(str(i+1)+") "+row[0])
            print("\n")
        elif command.startswith(extra_commands[1]):
            new_command = command.split();new_command.append("NONE")
            if len(new_command) < 4:
                print("\nList of 'Good' movies: ")
                c.execute("SELECT name FROM movieDataBase WHERE rating > 85 AND category != 'wli'");data = c.fetchall()
                for i,row in enumerate(data):
                    print(str(i+1)+") "+row[0])
                print("\nList of 'Ok' movies: ")
                c.execute("SELECT name FROM movieDataBase WHERE rating < 86 AND rating > 53 AND category != 'wli'");data = c.fetchall()
                for i,row in enumerate(data):
                    print(str(i+1)+") "+row[0])
                print("\nList of 'Bad' movies: ")
                c.execute("SELECT name FROM movieDataBase WHERE rating < 54 AND category != 'wli'");data = c.fetchall()
                for i,row in enumerate(data):
                    print(str(i+1)+") "+row[0])
                print("\n")
            elif new_command[2] == ('-g' or '-G'):
                print("\nList of 'Good' movies: ")
                c.execute("SELECT name FROM movieDataBase WHERE rating > 85 AND category != 'wli'");data = c.fetchall()
                for i,row in enumerate(data):
                    print(str(i+1)+") "+row[0])
                print("\n")
            elif new_command[2] == ('-k' or '-K'):
                print("\nList of 'Ok' movies: ")
                c.execute("SELECT name FROM movieDataBase WHERE rating < 86 AND rating > 53 AND category != 'wli'");data = c.fetchall()
                for i,row in enumerate(data):
                    print(str(i+1)+") "+row[0])
                print("\n")
            elif new_command[2] == ('-b' or '-B'):
                c.execute("SELECT name FROM movieDataBase WHERE rating < 54 AND category != 'wli'");data = c.fetchall()
                for i,row in enumerate(data):
                    print(str(i+1)+") "+row[0])
                print("\n")
        elif command.startswith(extra_commands[3]):
            new_command = command[7:]
            if new_command.isdigit():
                execute_string = "SELECT name FROM movieDataBase WHERE rating = {} AND category != 'wli'".format(new_command)
                c.execute(execute_string);data = c.fetchall()
                print("\nMovies with a rating of {}:".format(new_command))
                for i,row in enumerate(data):
                    print(str(i)+") "+row[0])
                print("\n")
            else:
                print("Not a valid entry for rating")
        elif command.startswith(extra_commands[2]):
            new_command = command[8:]
            execute_string = "SELECT rating FROM movieDataBase WHERE name = '{}'".format(new_command)
            c.execute(execute_string);data = c.fetchall();print("\nMovie Suggestion by rating: ")
            movie_rating = data[0][0];bounds = [movie_rating+2, movie_rating-2]
            execute_string = "SELECT name FROM movieDataBase WHERE rating > {} AND rating < {}".format(bounds[1], bounds[0])
            c.execute(execute_string);data = c.fetchall()
            for i,row in enumerate(data):
                if row[0] != new_command:
                    print(str(i)+") "+row[0])
            print("\n")
        else:
            print("I'm sorry, that command isn't available in this prompt")
    except Exception as e:
        print("Error at sort: "+str(e))

def search():
    '''searches for all the data
    on any specific movie'''
    global c, input_list

    extra_commands = ['ratings', 'movies', 'sorted', 'watch list']
    try:
        command = (input_list[-1])

        if command.startswith(extra_commands[0]):
            new_command = (command[7:]).strip()
            compound_new_command = command.split();compound_new_command.append("NONE")
            if compound_new_command[1] == 'all':
                string_command_rating = "SELECT rating, name FROM movieDataBase"
                if compound_new_command[2] == ('-o' or '-O'):
                    string_command_rating+=" ORDER BY rating DESC"
                if compound_new_command[2] == ('-p' or '-p'):
                    string_command_rating = "SELECT personal, name FROM movieDataBase ORDER by personal DESC"
                c.execute(string_command_rating);data = c.fetchall()
                print("\nThe ratings for the movies in the data base:")
                for i,row in enumerate(data):
                    print(str(i+1)+") "+str(row[0])+" --- "+row[1])
                print("\n")
            else:
                string_command_rating = "SELECT rating FROM movieDataBase WHERE name = '{}'".format(new_command)
                c.execute(string_command_rating);data = c.fetchall()
                print("The rating of {} is {}".format(new_command, str(data[0][0])))
        elif command == extra_commands[3]:
            print("\nMovies on your Watch List")
            c.execute("SELECT name FROM movieDataBase WHERE category = 'wli'");data = c.fetchall()
            for i,row in enumerate(data):
                print(str(i+1)+") "+row[0])
            print("\n")
        elif (extra_commands[0] and extra_commands[1]) not in command:
            string_command = "SELECT * FROM movieDataBase WHERE name = '{}'".format(command)
            c.execute(string_command);data = c.fetchall()
            print("\nName: "+data[0][0]);print("Rating: "+str(data[0][1]));print("Tags: "+data[0][3]);print("Category: "+data[0][4]+"\n") #change
        elif command.startswith(extra_commands[1]):
            print("\nMovies in Repository: ")
            c.execute("SELECT name FROM movieDataBase WHERE category != 'wli'");data = c.fetchall()
            for i,row in enumerate(data):
                print(str(i+1)+") "+row[0])
            print("\n")
        else:
            print("I'm sorry that command is not available in this module")
    except Exception as e:
        print("Error at search: "+str(e))

def stats():
    '''This prompt allows you to
    see various statistics within the db'''
    global c, input_list

    extra_commands = ['average', 'stan-dev']
    try:
        command = (input_list[-1])
        average_value = 0
        string_command_rating = "";cat_sel=""

        if command.startswith(extra_commands[0]):
            compound_new_command = command.split();compound_new_command.append("NONE")
            if len(compound_new_command) < 3:
                string_command_rating = "SELECT rating FROM movieDataBase";cat_sel = "Rating"
            elif compound_new_command[1] == ('-p' or '-P'):
                string_command_rating = "SELECT personal FROM movieDataBase";cat_sel = "Personal Rating"
            c.execute(string_command_rating);data = c.fetchall()
            print("\nThe Average {}: ".format(cat_sel))
            for row in data:
                average_value+=int(row[0])
            print("Value = {:.3f}".format(float(average_value/len(data))))
        if command.startswith(extra_commands[1]):
            print("\nThe Standard Deviation of the data is: ")
            c.execute("SELECT rating FROM movieDataBase");data = c.fetchall()
            for row in data:
                average_value+=int(row[0])
            mean = (float(average_value/len(data)));variance = 0.0
            for i in range(len(data)):
                variance+=float((i-mean)**2)
            SD = math.sqrt(variance/len(data))
            print("Value = {:.3f}".format(SD))
        else:
            print("I'm sorry, that command isn't available in this prompt")
    except Exception as e:
        print("Error at stats: "+str(e))

def create_dataBase():
    pass
    #c.execute("CREATE TABLE IF NOT EXISTS movieDataBase(name TEXT, rating INTEGER, personal INTEGER, tag TEXT, category TEXT)")

def main():
    '''run the main command
    prompt, is interactive'''
    global global_cmd_word, input_list, command_repository, c, conn
    print(INTRO)

    global_cmd_word = ""
    BaseCommand = True; PlayCMD = True
    input_list = []
    command_repository = {'help': 'helpf()', 'search': 'search()', 'new': 'new()', 'sort':'sort()', 'stats':'stats()'}

    conn = sqlite3.connect('movie.db')
    c = conn.cursor()

    while True:
        current_string = ("{}> ").format(global_cmd_word)
        raw_user_data = input(current_string)
        user_input = raw_user_data.strip()

        if user_input == 'quit':
            if conn:
                print("Cursor Closed")
                c.close()
            print("Exiting");break

        #Waiting to see if user invokes a base command
        if PlayCMD:
            if user_input in command_repository:
                process(user_input)
                BaseCommand = False
            else:
                print("Im sorry, '{}' isn't a registered command".format(str(user_input)))
        elif PlayCMD == False:
            if user_input == ('exit' or 'Exit'):
                global_cmd_word = ""
                BaseCommand = True
            else:
                input_list.append(user_input)
                exec(command_repository[global_cmd_word])

        PlayCMD = BaseCommand


if __name__ == '__main__':main()
