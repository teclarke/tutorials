def authorise_user(username):
  """
  Checks if a user is authorised in a csv file.
  Returns True if yes, False if no.
  """
  return True # for testing

def ask_for_user(user_number):
  """
  Asks the user to enter a username to play the game.
  """
  print(f"### Please enter an authorised username for user {user_number}. ###")
  user = input("Username: >")
  return user

def dice(sides):
  """
  Generates a random number between 1 and the number of sides provided.
  """
  import random
  wait = input(">> Press enter to roll dice. <<")
  print(">> Dice rolling... <<")
  number = random.randint(1,sides)
  return number

def calculate_score(roll_number, roll_score, prev_roll=0, current_round_score=0):
  """
  Calculates the total score for a particular round.
  If this is the user's first dice roll, roll_number=1.
  If roll_number=2, prev_roll contains the score of the previous roll.
  The score, roll_score from the dice roll is added to the total.
  Score is altered depending on scoring rules.
  """
  # Add roll_score to user total
  # current_round_score is used for double rolls
  round_score = current_round_score + roll_score
  print(f"## You rolled a {roll_score}! ##")
  # Scoring rules
  if roll_score % 2 == 0:
    round_score += 10
  else:
    round_score -= 5
  # Check for double roll on second round
  if roll_number == 2 and roll_score == prev_roll:
    print("## You rolled a double! Roll again. ##")
    roll_3 = calculate_score(3,dice(6), 0, round_score)
  else:
    return round_score

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
    # open results file
    with open(results_filename, "r") as r:
        dictionary_of_users = {}
        for line in r:
            # each user's score is on a different line, so split into name: score.
            users_score_list = line.strip("\n ").split(",")
            # put the users' names and scores into a dictionary
            dictionary_of_users.update({users_score_list[0]:int(users_score_list[1])})
        # sort the dictionary by score
        dictionary_of_scores = {value: key for key, value in dictionary_of_users.items()}
        list_of_scores = list(dictionary_of_scores.items())
        dictionary_of_scores = dict(sorted(list_of_scores,reverse=True))

    # displaying the top 5 results to the user
    if dictionary_of_scores == {}:
        print("## The scoreboard is empty. Be the first player to win! ##")
    else:
        print("## The scoreboard now stands as... ##\n")
        displayed = 0
        while displayed < 5 and displayed < len(dictionary_of_scores):
            for score, user in dictionary_of_scores.items():
                print(str(displayed+1)+".","##", user, "with", score, "points. ##")
                displayed += 1


def gameplay(user_1, user_2,number_of_rounds=5):
  """
  Runs only once authorise_user() is True.
  Co-ordinates scoring and dice-rolling.
  Tracks user scores and number of rounds played.
  """
  """authorised_u1, authorised_u2 = (False,)*2
  while not authorised_u1 and not authorised_u2:
    # Checks if users 1 and 2 are authorised using authorise_user()
    authorised_u1, authorised_u2 = authorise_user(user_1), authorise_user(user_2)
    # Asks the user for another username if wrong.
    if not authorised_u1:
      print(">> User 1 not authorised. <<")
      user_1 = ask_for_user("1")
    if not authorised_u2:
      print(">> User 2 not authorised. <<")
      user_2 = ask_for_user("2")
    """
  # Once all users are authorised, gameplay starts.
  print("\n### Users", user_1, "and", user_2, "are playing. ###")
  users = [user_1,user_2]
  # Repeats for the number of rounds required
  scores = [0,0]
  for rounds in range(number_of_rounds):
    print("\n################################")
    print("## Welcome to round", str(rounds+1) +"! ##")
    # Displays scores so far
    print("The current scores are:")
    print(user_1, scores[0], "-", scores[1], user_2)
    # Repeats gameplay process for each user
    for i in range(2):
      print()
      print("## It's", users[i] + "'s turn! ##")
      # Rolls dice and calculates score
      for roll in range(2):
        scores[i] += calculate_score(roll,dice(6))
        if scores[i] < 0: scores[i] = 0
        print(f"## That makes your score {scores[i]}! ##")
  print("\n################################")
  print("## End of Game ##")
  print("The final scores are:")
  print(user_1, scores[0], "-", scores[1], user_2)
  winner = users[scores.index(max(scores))]
  print(f"## The winner of the game is {winner} with {max(scores)} points! ##")
  save_results(winner,max(scores))
  scoreboard()

### Run code ###
print("### Welcome to OCR Dice Game! ###")
scoreboard()
#gameplay(ask_for_user("1"), ask_for_user("2"))
gameplay("Tom","Bob",1)
