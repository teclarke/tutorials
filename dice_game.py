from time import sleep
def ask_for_user(user_number):
  """
  Asks the user to enter a username to play the game.
  """
  print(f"\n### Please enter an authorised username for user {user_number}. ###")
  user = input("Username: >")
  return user

def authorise_user(user_number, filename="users.txt"):
  """
  Asks for user from ask_for_user.
  Checks if a user is authorised in a txt file.
  Returns True if yes, False if no.
  """
  username = ask_for_user(user_number)
  try:
      with open(filename,"r") as u:
          for line in u:
              if username.strip("\n ") == line.strip("\n ") and username != "":
                  print("## You're in! ##")
                  return True,username
              else:
                  continue
      if username == "":
          return False, username
      else:
          print(f"\n## User {username} is not authorised. ##")
          print(f"## Add user {username} to user directory? ##")
          print("(type anything for yes)")
          adduser = input("(press enter) No >>")
          if adduser != "":
              with open(filename, "a") as a:
                  a.write("\n"+username)
                  return True,username
          else:
              return False,username
  except FileNotFoundError:
        print("## No authorised users found. ##")
        print(f"## Create user list with user {username} anyway? ##")
        print("(type anything to cancel game)")
        createnew = input("(press enter) Yes >>")
        if createnew == "":
            with open(filename,"w+") as u:
                u.write(username)
                return True

def dice(sides):
  """
  Generates a random number between 1 and the number of sides provided.
  """
  import random
  wait = input(">> Press enter to roll dice. <<")
  print(">> Dice rolling... <<")
  number = random.randint(1,sides)
  print(f"You rolled a {number}!")
  return number

def calculate_score(roll_1,roll_2,current_round_score=0,roll_3=0): # roll_number, roll_score, prev_roll=0, current_round_score=0
  """
  Calculates the total score for a particular round.
  If this is the user's first dice roll, roll_number=1.
  If roll_number=2, prev_roll contains the score of the previous roll.
  The score, roll_score from the dice roll is added to the total.
  Score is altered depending on scoring rules.
  """
  for roll_score in [roll_1, roll_2,roll_3]:
      # Add roll_score to user total
      # current_round_score is used for double rolls
      current_round_score += roll_score
      # Scoring rules
      if roll_score != 0:
          if roll_score % 2 == 0:
            current_round_score += 10
          else:
            current_round_score -= 5
      # Check for double roll on second round
  if roll_1 == roll_2 and roll_1 != 0 and roll_2 != 0:
        print("## You rolled a double! Roll again. ##")
        current_round_score = calculate_score(0,0,current_round_score,dice(6))
  return current_round_score

def save_results(winner, winner_score):
  print("\n################################")
  print("## Saving results... ##")
  with open("results.txt", "a") as r:
    print(winner+","+str(winner_score),file=r)
  print("## Results saved successfully ##")


def scoreboard(results_filename="results.txt"):
    """
    Displays the top 5 scores from the results.txt file.
    """
    try:
      # open results file
      with open(results_filename, "r") as r:
          dictionary_of_users = {}
          for line in r:
              # each user's score is on a different line, so split into name: score.
              users_score_list = line.strip("\n ").split(",")
              # put the users' names and scores into a dictionary
              if users_score_list[0] in dictionary_of_users.keys():
                  user_curr_score = dictionary_of_users[users_score_list[0]]
              else:
                  user_curr_score = 0
              dictionary_of_users.update({users_score_list[0]:max([int(users_score_list[1]),user_curr_score])})
          # sort the dictionary by score
          dictionary_of_scores = {value: key for key, value in dictionary_of_users.items()}
          list_of_scores = list(dictionary_of_scores.items())
          dictionary_of_scores = dict(sorted(list_of_scores,reverse=True))
    except FileNotFoundError:
      scoreboard = open("results.txt","w+")
      dictionary_of_scores = {}
    # displaying the top 5 results to the user
    if dictionary_of_scores == {}:
        print("## The scoreboard is empty. Be the first player to win! ##")
    else:
        print("## The scoreboard currently stands as... ##\n")
        displayed = 0
        while displayed < 5 and displayed < len(dictionary_of_scores):
            for score, user in dictionary_of_scores.items():
                print(str(displayed+1)+".","##", user, "with", score, "points. ##")
                displayed += 1
    sleep(2)

def gameplay(number_of_rounds=5):
  """
  Runs only once authorise_user() is True for both players.
  Co-ordinates scoring and dice-rolling.
  Tracks user scores and number of rounds played.
  """
  """
  scoreboard()
  authorised_u1, authorised_u2 = (False,)*2
  while not authorised_u1:
    # Checks if user 1 is authorised using authorise_user()
    authorised_u1,user_1 = authorise_user("1")
  while not authorised_u2:
    # as above for user 2
    authorised_u2,user_2 = authorise_user("2")


  # Once all users are authorised, gameplay starts.
  print("\n### Users", user_1, "and", user_2, "are playing. ###")

  users = [[user_1,0],[user_2,0]] # co-ordinates  with the list below
  """
  users = [["jim789",0],["geoff012",0]]
  # Repeats for the number of rounds required
  for rounds in range(number_of_rounds):
    print("\n################################")
    print("## Welcome to round", str(rounds+1) +"! ##")
    # Displays scores so far
    print("The current scores are:")
    print(users[0][0], users[0][1], "-", users[1][1], users[1][0])
    # Repeats gameplay process for each user
    for i in range(2):
      print("\n## It's", users[i][0] + "'s turn! ##")
      # Rolls dice and calculates score
      users[i][1] += calculate_score(dice(6),dice(6))
      if users[i][1] < 0: users[i][1] = 0
      print(f"## That makes your score {users[i][1]}! ##")
  print("\n################################")
  print("## End of Game ##")
  print("The final scores are:")
  print(users[0][0], users[0][1], "-", users[1][1], users[1][0])
  winner_score= max([users[0][1],users[1][1]])
  for scores in users:
      if winner_score in scores:
          winner_name = scores[0]

  print(f"## The winner of the game is {winner_name} with {winner_score} points! ##")
  save_results(winner_name,winner_score)
  scoreboard()

### Run code ###
playing = True
while playing:
  print("\n\n\n### Welcome to OCR Dice Game! ###")
  gameplay(1)
  print("\n################################")
  print("# Type anything to end gameplay.")
  again = input("# Press enter to play again. >>")
  playing = True if again == "" else False
