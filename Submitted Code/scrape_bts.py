import applescript
import os
import time

target_site = "https://www.transtats.bts.gov/AverageFare/"

# start by setting the date and quarter correctly
# press submit
# download data
# repeat



# go through each year
for year in range(2020, 2024):

    set_fields_year = '''
        set desiredOptionValue to "''' + str(year) + '''"

            tell active tab of window 1
                execute javascript "
                    var dropdownOptions = document.querySelectorAll('select[name=\\"dlstYear\\"] option');
                    
                    for (var i = 0; i < dropdownOptions.length; i++) {
                        if (dropdownOptions[i].value === '" & desiredOptionValue & "') {
                            dropdownOptions[i].selected = true;
                            break;
                        }
                    }
                    
                "
            end tell
        '''
        
    # setting the year field
    print(f"NEW YEAR: {year}")

    applescript.tell.app("Google Chrome", set_fields_year)
    time.sleep(2)
    applescript.tell.app("Google Chrome", set_fields_year)
    time.sleep(2)
    applescript.tell.app("Google Chrome", set_fields_year)
    time.sleep(5)

    # go through each quarter
    for quarter in range(5):

        set_fields_quarter = '''
            set desiredOptionValue to "''' + str(quarter) + '''"

                tell active tab of window 1
                    execute javascript "
                        var dropdownOptions = document.querySelectorAll('select[name=\\"dlstQuarter\\"] option');
                        
                        for (var i = 0; i < dropdownOptions.length; i++) {
                            if (dropdownOptions[i].value === '" & desiredOptionValue & "') {
                                dropdownOptions[i].selected = true;
                                break;
                            }
                        }
                        
                    "
                end tell
            '''

        submit_request = '''
            tell active tab of window 1
                execute javascript "document.getElementById('btnSubmit').click();"
            end tell'''

        download_data = '''
            tell active tab of window 1
                execute javascript "document.getElementById('Button1').click();"
            end tell
            '''

        # setting the quarter field

        print(f"NEW QUARTER: {quarter}")

        applescript.tell.app("Google Chrome", set_fields_quarter)
        time.sleep(2)
        
        applescript.tell.app("Google Chrome", set_fields_quarter)
        time.sleep(2)
        
        applescript.tell.app("Google Chrome", set_fields_quarter)
        time.sleep(5)

        # applescript.tell.app("Google Chrome", submit_request)

        # time.sleep(15)

        applescript.tell.app("Google Chrome", download_data)

        time.sleep(15)