import Login
import NewsManagment
from Login import User, cursor, conn
import Profile
from NewsManagment import NewsManager, api_url2, articles_isEmpty
from Recomendations import fetch_articles, get_recommendations, fetch_potential_articles

if __name__ == "__main__":
    deleted = False
    while True:
        while True:
            choice = 0
            print("====================================")
            print("       Welcome to WhatsNew       ")
            print("====================================")
            print("1. Login")
            print("2. Create Account")
            print("3. Forgot Password")
            print("4. Forgot Username")
            print("5. Exit")

            try:
                choice = int(input("Select Option: "))
            except ValueError:
                print("Invalid input please try again")
                continue
            if choice == 1:
                user: User = Login.login()
                if user is None:
                    continue
            elif choice == 2:
                Login.create_account()
                continue
            elif choice == 3:
                Profile.forgot_password(cursor,conn)
                continue
            elif choice == 4:
                Profile.forgot_username(cursor,conn)
                continue
            elif choice == 5:
                exit()
            else:
                print("Please type 1, 2, 3, 4, or 5.")
                continue
            break
        print()
        print("Welcome!")
        #Main loop
        while True:
            print("=============================")
            print("        Dashboard       ")
            print("=============================")
            print("1) View Latest News")
            print()
            print("2) Search News")
            print()
            print("3) Saved News")
            print()
            print("4) Recommendations")
            print()
            print("5) Preferences")
            print()
            print("6) Profile Settings")
            print()
            print("7) Logout")
            print()
            print("8) Exit")
            option = int(input("Select Option: "))

            match option:
                case 1:
                    print("Latest news: ")
                    articles = NewsManagment.print_article(api_url2, page_size=user.profile.page_size)
                    NewsManagment.prompt_articles_save(articles, user)
                    continue
                case 2:
                    search = input("What would you like to find? ")
                    articles = user.profile.new_manager.search_articles(search,user.profile.page_size)
                    NewsManagment.prompt_articles_save(articles, user,)
                case 3:
                    while True:
                        if NewsManagment.articles_isEmpty(user.profile.saved_articles,user):
                            print("Your list is empty")
                            break
                        for i, article in enumerate(user.profile.saved_articles, start=1):
                            print(f"{i}. {article}")
                        save_article_choice = input("Enter spaced article numbers to remove OR type 'no' to go back: ").strip().lower()
                        if save_article_choice == "no":
                            break
                        user.profile.new_manager.remove_articles(save_article_choice,user)
                        for i, article in enumerate(user.profile.saved_articles, start=1):
                            print(f"{i}. {article}")
                        continue
                case 4:
                    if articles_isEmpty(user.profile.article_preferences,user):
                        print("Your preference list is empty. Please enter your preferences in option 5,", end= " ")
                        print("So we can fetch proper recommendations for you.")
                        continue
                    print("Fetching Recommendations...")
                    potential_articles = fetch_potential_articles(user.profile.article_preferences,user.profile.page_size)
                    recommendations = get_recommendations(user.profile.saved_articles,potential_articles)
                    if not recommendations:
                        print("No recommendations found")
                        continue
                    for i, article in enumerate(recommendations,start =1):
                        print(f"{i}) {article}")
                    NewsManagment.prompt_articles_save((recommendations,{}),user)
                case 5:
                    preferences = input("What types of articles do you wish to see (comma separated): ").lower().strip().split(",")
                    user.profile.article_preferences = preferences
                    user.profile.new_manager.filter_topics(user.profile.article_preferences)
                    continue
                case 6:
                    while True:
                        print("1) Change Email")
                        print()
                        print("2) Change Password")
                        print()
                        print("3) Change Username")
                        print()
                        print("4) Delete Account")
                        print()
                        print("5) Change Page Size")
                        print()
                        print("6) Back")
                        options = int(input("Select option: "))
                        match options:
                            case 1:
                                user.profile.change_email(cursor,conn)
                                continue
                            case 2:
                                user.profile.change_password(cursor,conn)
                                continue
                            case 3:
                                user.profile.change_username(user,cursor,conn)
                                continue
                            case 4:
                                while True:
                                    confirm = input(
                                        "Are you sure? All data will be deleted. (Type yes or no): ").lower()
                                    if confirm == "yes":
                                        user.profile.delete_profile(cursor, conn)
                                        deleted = True
                                        break
                                    elif confirm == "no":
                                        break
                                    else:
                                        print("Please type yes or no")
                                if deleted:
                                    break  # breaks dashboard loop
                            case 5:
                                user.profile.change_page_size()
                                continue
                            case 6:
                                break
                case 7:
                    break
                case 8:
                    exit()
                case _:
                    print("Please type the available options.")
            if deleted:
                break
