from prawcore.exceptions import RequestException, ServerError
import re
from Reddit import reddit
import time
from utils import (
    SignalHandler,
    blockRedditor,
    cakedayCheck,
    commentCheck,
    downloadNewSubtitles,
    getActiveSubs,
    inboxCheck,
    replyToComment,
)
from quotes import (
    bhendiCount,
    happyCakeday,
    randomQuote,
    shutupSaiman,
)


signalHandler = SignalHandler()


def main():

    downloadNewSubtitles()

    commentCheckTime = 0
    inboxCheckTime = 0
    me = reddit.user.me()

    for comment in reddit.subreddit(getActiveSubs()).stream.comments():

        signalHandler.loopStart()

        if time.time() > inboxCheckTime:
            inboxCheck()
            inboxCheckTime = time.time() + 3600 * 12

        if time.time() > commentCheckTime:
            commentCheck()
            commentCheckTime = time.time() + 1800

        if comment.saved \
                or comment.author == me \
                or re.search(r"\bre+post\b", comment.body, re.I):
            continue

        if re.search(r"\b(chup|shut ?(the)? ?(fuck)? ?up|stop)\b",
                     comment.body, re.I) \
                and comment.parent().author == me:
            print(f"Replying to '{comment.permalink}' with shutupSaiman")
            replyToComment(comment, shutupSaiman())

        elif cakedayCheck(comment):
            print(f"Replying to '{comment.permalink}' with Cakeday")
            replyToComment(comment, happyCakeday())

        elif re.search(
            r"\bBh[ei]+ndi\b|\bSai(man)?-?(Said| ?bot)\b|\bTimothy\b",
                comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with random quote")
            replyToComment(comment, randomQuote())

        elif re.search(r"bhendicount", comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with bhendi count")
            replyToComment(comment, bhendiCount(comment))

        elif re.search(r"!(ignore|block)", comment.body, re.I):
            if comment.parent.author == me:
                blockRedditor(comment.author)

        elif re.match(r"b ?i ?n ?o ?d", comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with binod")
            replyToComment(comment, "[Very Cringe](https://redd.it/i6i454)")

        signalHandler.loopEnd()


if __name__ == "__main__":
    print("Starting the bot")
    while(True):
        try:
            main()
        # Network Issues
        except (RequestException, ServerError) as e:
            print(e)
            time.sleep(60)
        else:
            print("Program ended. It aint supposed to")
            break
