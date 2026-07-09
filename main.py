
import Login
import NewsManagment
import Profile
from NewsManagment import NewsManager, api_url2, articles_isEmpty, Article
from Recomendations import get_recommendations, fetch_potential_articles
from dotenv import load_dotenv
load_dotenv()
def prompt_save_articles(ids,user):
    ask_to_save_articles = input("Are there articles you wish to save? (yes/no): ").strip().lower()
    if ask_to_save_articles == "yes":
        try:
            choices_input = input("Enter the numbers of the articles you wish to save (separated by spaces): ").strip()
            save_article_choice = [int(x) for x in choices_input.split()]
            if save_article_choice:
                NewsManager.save_articles(save_article_choice, ids, user)
                print(f"{len(save_article_choice)} articles saved to your profile!")
            else:
                print("No valid article numbers entered.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")
    else:
        print("No articles saved.")

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
                user: Login.User = Login.login()
                if user is None:
                    continue
            elif choice == 2:
                Login.create_account()
                continue
            elif choice == 3:
                Profile.forgot_password()
                continue
            elif choice == 4:
                Profile.forgot_username()
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
                    articles = NewsManagment.fetch_articles(api_url2,page_size=user.profile.page_size)
                    ids = {}
                    for i, article in enumerate(articles, start=1):
                        print(f"{i}) {article}")
                        ids[i] = article
                    print(f"{len(articles)} articles found")
                    prompt_save_articles(ids, user)
                    continue
                case 2:
                    search = input("What would you like to find? ")
                    ids = {}
                    articles = NewsManager.search_articles(search,user.profile.page_size)
                    for i, article in enumerate(articles, start=1):
                        print(f"{i}) {article}")
                        ids[i] = article
                    print(f"{len(articles)} articles found")
                    prompt_save_articles(ids, user)
                case 3:
                    while True:
                        user_saved_articles = NewsManager.get_saved_articles(user.id)
                        if NewsManagment.articles_isEmpty(user_saved_articles):
                            print("Your list is empty")
                            break
                        ids = {}
                        for i, article in enumerate(user_saved_articles, start=1):
                            print(f"{i}. {article['title']}\n{article['source']}\n{article['url']}\n")
                            ids[i] = article["id"]
                        save_article_choice = input("Enter spaced article numbers to remove OR type 'no' to go back: ").strip().lower()
                        if save_article_choice == "no":
                            break
                        NewsManager.remove_articles(save_article_choice,ids)
                        continue
                case 4:
                    if articles_isEmpty(NewsManager.get_preferences(user.id)):
                        print("Your preference list is empty.\nPlease enter your preferences in option 5,", end= " ")
                        print("So we can fetch proper recommendations for you.")
                        continue
                    print("Fetching Recommendations...")
                    get_saved_articles = NewsManager.get_saved_articles(user.id)
                    get_preferences = NewsManager.get_preferences(user.id)
                    saved_articles_list = []
                    preferences_list = []
                    for articles in get_saved_articles:
                        article = Article(
                            id = articles["id"],
                            title = articles["title"],
                            source= articles["source"],
                            publishedAt= None,
                            url = articles["url"],
                            topic= None,
                            author= None
                        )
                        saved_articles_list.append(article)

                    for articles in get_preferences:
                        preferences_list.append(articles["topic"])

                    potential_articles = fetch_potential_articles(preferences_list,user.profile.page_size)
                    recommendations = get_recommendations(saved_articles_list,potential_articles)
                    if not recommendations:
                        print("No recommendations found")
                        continue
                    for i, article in enumerate(recommendations,start =1):
                        print(f"{i}) {article}")
                    rec_ids = {i: article for i, article in enumerate(recommendations, start=1)}
                    prompt_save_articles(rec_ids, user)
                case 5:
                    preferences = input("What types of articles do you wish to see (comma separated): ").lower().strip().split(",")
                    NewsManager.update_preferences(preferences,user.id)
                    result = NewsManager.filter_topics(preferences)
                    if len(preferences) == 1:
                        print(f"{result} is your preference")
                    else:
                        print(f"{result} are your preferences")
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
                                user.profile.change_email()
                                continue
                            case 2:
                                user.profile.change_password()
                                continue
                            case 3:
                                user.profile.change_username(user)
                                continue
                            case 4:
                                while True:
                                    confirm = input(
                                        "Are you sure? All data will be deleted. (Type yes or no): ").lower()
                                    if confirm == "yes":
                                        user.profile.delete_profile()
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