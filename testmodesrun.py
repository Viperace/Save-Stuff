
from django.utils import timezone
import pytz
if __name__ == '__main__':
    # Run only once. Dont keep running
    # 这里是创建300个假用户.执行一次就可以.
    # for ind in xrange(0, 300):
    #  cuser()

    # Get the current index
    start_index = 6300.00

    ###################################
    # Listen for bet from player
    ###################################
    # Model fake betting
    userid_list = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7"]

    # Reset all
    # bettingup.objects.all().delete()
    for test_telid in userid_list:
        # Get user information
        x = Extend_user.objects.get(ext_user_id=test_telid)

        # Simulate time
        timezone.now()
        bet_time = datetime.datetime(2018, 7, 18, 5, 13, 21, tzinfo=pytz.timezone('Asia/Shanghai'))

        # Simulate size
        bet_size = random.randint(20, 50) * 10

        # Simulate direction
        bet_isUp = random.randint(0, 100) > 50

        # Simulate place bet
        if bet_isUp:
            existing_bettor = bettingup.objects.filter(userid=test_telid)

            # If existing, then topup
            if existing_bettor.count() > 0:
                bettor = bettingup.objects.get(userid=test_telid)
                bettor.betquota += bet_size  # Add more !
                bettor.save()
                print str(bettor.telid) + " top up bet"
            else:
                # Create entry
                bettingup.objects.get_or_create(userid=x.id, telid=x.telid, betquota=bet_size, bettime=bet_time)
        else:
            existing_bettor = bettingdwon.objects.filter(userid=test_telid)

            # If existing, then topup
            if existing_bettor.count() > 0:
                bettor = bettingdwon.objects.get(userid=test_telid)
                bettor.betquota += bet_size  # Add more !
                bettor.save()
                print str(bettor.telid) + " top up bet"
            else:
                # Create entry
                bettingdwon.objects.get_or_create(userid=x.id, telid=x.telid, betquota=bet_size, bettime=bet_time)

        print x.telid + " bet " + str(bet_size) + " On up: " + str(bet_isUp)


    ###################################
    # Aggregate Result
    ###################################
    # Get result
    end_index = 6500.00

    # Allocate reward

    #

    print "Program end"
