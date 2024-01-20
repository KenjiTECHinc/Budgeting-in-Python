import sys
import datetime
#--------------------------Global Functions--------------------------
def save_logs(logbook, my_amount):
    """ for saving records."""
    try:
        r = open("records.txt", 'w')
        f = open("Account.txt", 'w')
        r.write(str(logbook))
        r.close()
        f.write(str(my_amount))
        f.close()
        
    except OSError as err:
        sys.stderr.write("Save Error!: {}\n".format(err))
    return

def read_account():
    """read account."""
    try:
        with open("Account.txt", 'r') as f:
            my_amount=f.read()
        if my_amount == '':
            return 0
        else:
            return my_amount
    except OSError as err:
        sys.stderr.write("File error, failed to sync account!\nError!: {}\n".format(err))
    return

def new():
    """Welcome prompt"""
    print("Hi, new user!")
    init_name = str(input("How should I call you? "))
    try:
        init_amount=int(input("Nice to meet you, {}! How much money do you have? ".format(init_name)))
    except ValueError:
        sys.stderr.write("Invalid value for money. Set to 0 by default\n") ##assignment
        init_amount = 0
    save_user(init_amount, init_name)
    return init_amount, init_name

def save_user(init_amount, init_name): 
    """save user to file"""
    try:
        with open("Account.txt", 'w') as f:
            f.write(str(init_amount))
        with open("Username.txt", 'w') as u:
            u.write(str(init_name))
        return
    except OSError as err:
        sys.stderr.write("Error!: {}\n".format(err))
    return

def get_user():
    """get user's info."""
    try:
        with open("Username.txt", 'r') as u:
            user = u.read()
        return user
    except OSError as err:
        sys.stderr.write("File not found, failed to acquire username! Set to default name.\nError!: {}\n".format(err))
        return 'User'

def read_book():
    """read records"""
    try:
        with open("records.txt", 'r') as r:
            logbook=r.read()
        if logbook != '':
            try:
                temp = logbook.split(',')
                temp.pop()
                for item in temp:
                    item = item.split()
                    assert int(len(item)) == 5
            except AssertionError:
                sys.stderr.write("File Format Error! removed all logs, please reset account.")
                logbook = ''
        return logbook
    except OSError as err:
        sys.stderr.write("File error, failed to acquire log history!\nError!: {}\n".format(err))
    return

def clear_user():
    """ clear user's info."""
    try:
        f = open("Account.txt", "w")
        f.write('N')
        f.close()
        r = open("records.txt", 'w')
        r.write('')
        r.close()
        u = open("Username.txt", 'w')
        u.write('')
        u.close()
        s = open("Setting.txt", 'w')
        s.write('1')
        s.close()
    except OSError as err:
        sys.stderr.write("Error!: {}\n".format(err))
    return

def read_setting():
    '''read setting text'''
    try:
        with open("Setting.txt", 'r') as r:
            preset = r.read()
        assert preset != ''
        assert int(preset) == 1 or int(preset) == 0
        return int(preset)
    except AssertionError:
        sys.stderr.write("File Error, set to default!")
        return 1
    except (TypeError, ValueError):
        sys.stderr.write("File Error, set to default!")
        return 1
    except OSError:
        sys.stderr.write("File Error, unable to read. Fix required!")

def save_setting(date):
    '''save setting'''
    try:
        with open("Setting.txt", 'w') as r:
            r.write(str(date))
    except OSError as err:
        sys.stderr.write("Error!: {}".format(err))
    return
#--------------------------Class Record---------------------------
class Record:
    def __init__(self, category, name, amount):
        '''init record'''
        self._category = category
        self._name = name
        self._amount = amount
        self._date = str(datetime.datetime.now())
        return
    
    @property
    def get_category(self):
        '''get category'''
        return self._category
    
    @property
    def get_name(self):
        '''get name'''
        return self._name
    
    @property
    def get_amount(self):
        '''get amount'''
        return self._amount
    
    @property
    def get_date(self):
        '''get date'''
        return self._date
    
#--------------------------Class Records--------------------------
class Records:
    def __init__(self):
        '''init account'''
        self._amount = read_account()
        if self._amount == "N" and int(len(self._amount)) == 1:
            self._amount, self._name = new()
            
        elif self._amount.isdigit():
            self._name = get_user()

        else:
            sys.stderr.write("Error! Set to default!\n")
            self._amount = 0
            self._name = 'User'
        self._logbook = read_book()
        self._showdate = read_setting()
        return
    
    def add(self, change): #NOTE: Make sure cannot add categories not within list.
        """Add new log prompt"""
        #change=input("Add an expense or income record with description and amount: ") 
        temp_amount = change.split(', ')
        cnt = succnt = 0
        for items in temp_amount:
            try:
                items_temp=items.split()
                record_temp = Record(items_temp[0], items_temp[1], items_temp[2])
                if cat.valid_cat(cat._category, record_temp._category) == 1:
                    self._amount = int(self._amount) + int(record_temp.get_amount)
                    self._logbook = self._logbook + " ".join([str(items), str(record_temp.get_date)]) + ','
                    succnt+=1
                else:
                    sys.stderr.write("Category does not exist. Must be in an existing category.\n")
            except (IndexError, ValueError):
                sys.stderr.write("Wrong format for '{}'.\nThe format should be like this: category description +/-amount. Failed to log item!\n".format(items))
            cnt+=1
        save_logs(self._logbook, self._amount)
        print("\nSuccessfully processed {}/{} items!\n".format(succnt,cnt))
        return
    
    @property
    def exit(self):
        """Exit function"""
        while True:
            exit_flag = str(input("\nAre you sure you want to exit?: Y / N ")) #confirm user want to quit.
            if exit_flag in 'Yy':
                save_setting(self._showdate)
                return 1
            elif exit_flag in 'Nn':
                print("\ncanceled!\n")
                return 2
            else:
                sys.stderr.write("Sorry, this command is invalid. Please try again!\n")
        return
    
    @property
    def reset(self):
        """Reset function"""
        print("\nWARNING: Resetting account means you will have to exit the program and restart!\n")
        while True:
            reset_signal = str(input("Are you sure, you want to reset account?: Y / N ")) #type Y or N to reset or not reset.
            if reset_signal in 'Yy':
                clear_user()
                return 1
            elif reset_signal in 'Nn':
                print("\ncanceled!\n")
                return 2
            else:
                sys.stderr.write("Sorry, this command is invalid. Please try again!\n")
        return
    
    def view_date(self, my_amount, logbook):
        """View records function"""
        if type(logbook) == str:
            temp_book = logbook.split(',')
            temp_book.pop() #pop the last element that is ''
        elif type(logbook) in {list, tuple}:
            temp_book = logbook
        else:
            sys.stderr.write("Type error! Unable to view.")
        print("\nHere are your records:\nCategory       Log                  Amount     Date-Time\n====================================================================\n")
        for log in temp_book: #category space = 15.
            log = log.split()
            spacing = 15 - int(len(log[0]))
            print("{}".format(log[0]) + "_"*spacing, end='') #print category
            spacing = 20 - int(len(log[1]))
            print("{}".format(log[1]) + "_"*spacing, end='') #print description
            spacing = 10 - int(len(log[2]))
            print(" {}".format(log[2]) + "_"*spacing, end='') #print record
            print(" {}".format(log[3]), end=' ') #print date
            print("{}".format(log[4])) #print time
        print("\n====================================================================\n")
        print("Total balance: {}\n".format(my_amount))
        return
    
    def view(self, my_amount, logbook):
        """View records function"""
        if type(logbook) == str:
            temp_book = logbook.split(',')
            temp_book.pop() #pop the last element that is ''
        elif type(logbook) in {list, tuple}:
            temp_book = logbook
        else:
            sys.stderr.write("Type error! Unable to view.")
        print("\nHere are your records:\nCategory       Log                  Amount\n================================================\n")
        for log in temp_book: #category space = 15.
            log = log.split()
            spacing = 15 - int(len(log[0]))
            print("{}".format(log[0]) + "_"*spacing, end='') #print category
            spacing = 20 - int(len(log[1]))
            print("{}".format(log[1]) + "_"*spacing, end='') #print description
            spacing = 10 - int(len(log[2]))
            print(" {}".format(log[2])) #print record
        print("\n================================================\n")
        print("Total balance: {}\n".format(my_amount))
        return
    
    @property
    def find(self):
        '''function to find the records of specific search'''
        key = input('Input category: ')
        temp_book = self._logbook.split(',')
        temp_book.pop() #pop the ',' out
        cnt=0
        for item in temp_book:
            temp_book[cnt]=item.split() 
            cnt+=1
        key_list = cat.find_subcategories(key, cat._category)
        filtered_list = list(filter(lambda item: item[0] in key_list, temp_book)) #filter returns address of filtered list.
        cnt = temp_amount = 0
        for i in filtered_list:
            temp_amount += int(i[2])
            filtered_list[cnt] = ' '.join(i)
            cnt+=1
        self.view(temp_amount, filtered_list) #remove redundancy by passing the list as parameter into a view function instead
        return 
    
    @property
    def delete(self):
        """Delete function, search keyword to delete"""
        temp_book = self._logbook.split(',') 
        temp_book.pop()
        print("\nWhich log would you like to remove?")
        target = str(input("Type the description with or without amount: "))
        count = 0
        temp_keep = list()
        for search in temp_book: #search log book
            temp_search = search.split() #split search, shallow copy
            if target == (temp_search[1] or temp_search[2]): #if found same keyword then append!
                temp_keep.append(search)
                count +=1

        ##check the amount of similar keywords
        if count == 1: #if count is 1 then immediately replace it with blank space.
            delete = temp_keep[0] + ','
            delete_amount = temp_keep[0].split()
            self._amount = int(self._amount) - int(delete_amount[2])
            self._logbook = self._logbook.replace(delete, '')
            save_logs(self._logbook, self._amount) #send to function for saving (reduce lines)
            print("\nSaved!\n")
            return

        elif count > 1: #else if count is more than 1 then user must select.
            print("\nWe found more than one log! please select one that you would like to delete:")
            print("=============================================================================")
            cntLog = 0
            for log in temp_keep: #list all the logs found with same keyword
                log_temp = log.split()
                if self._showdate == 1:
                    print("({:d}): {} {} {} {}  Category: {}".format(cntLog,log_temp[1],log_temp[2],log_temp[3],log_temp[4],log_temp[0]))
                elif self._showdate == 0:
                    print("({:d}): {} {}  Category: {}".format(cntLog,log_temp[1],log_temp[2],log_temp[0]))
                cntLog +=1
            deleteLog = input("Please select a number or type 'all' / 'cancel': ")
            try:
                if deleteLog != 'all' and deleteLog != 'cancel' and int(deleteLog) < cntLog: #'number selected' case
                    delete = temp_keep[int(deleteLog)] #get the value of the key selected
                    delete_amount = temp_keep[int(deleteLog)].split()
                    self._amount = int(self._amount) - int(delete_amount[2]) #restore account's balance
                    self._logbook = self._logbook.split(',')
                    for find_delete in self._logbook: #find the key
                        if delete in find_delete:
                            self._logbook.pop(self._logbook.index(find_delete)) #remove key from file
                            break
                        else:
                            pass
                    self._logbook = ','.join(self._logbook) #rejoin list before sending to function
                    save_logs(self._logbook, self._amount)
                    print("\nSaved!\n")
                    return
                elif deleteLog == 'all': #'all' case, program will delete all logs that has the same keyword.
                    for find_delete in temp_keep:
                        delete_amount = find_delete.split()
                        self._amount = int(self._amount) - int(delete_amount[2])
                        self._logbook = self._logbook.replace(find_delete + ',', '')
                    save_logs(self._logbook, self._amount)
                    print("\nSaved!\n")
                    return
                elif deleteLog == 'cancel': #'cancel' case, program will not perform any delete action
                    print("\nCanceled!\n")
                    return
            except:
                sys.stderr.write("Sorry, invalid input. Please try again later!\n")
                return
        else: #else just quit
            sys.stderr.write("Log not found!\n")
            return
        return
    
    @property
    def settings_welcome(self):
        '''first page of setting'''
        self.settings_view
        while True:
            changes = str(input("\nEdit Settings? Y/N: ")).lower()
            if changes in ('n', 'N'):
                break
            elif changes in ('y','Y'):
                self.settings_edit()
                continue
            else:
                sys.stderr.write("Invalid command. Please try again!")
                continue
        return
    
    @property
    def settings_view(self):
        '''print format'''
        print("\nSETTINGS\n===============")
        print("Date: ", end = '')
        if self._showdate == 1:
            print("▣ ON    ◻ OFF")
        else:
            print("◻ ON    ▣ OFF")
        return
    
    
    def settings_edit(self):
        '''edit setting'''
        while True:
            changes = str(input("Please input settings and preference ('cancel' to exit): ")).lower()
            if changes == 'cancel':
                break
            else:
                try:
                    changes_temp = changes.split()
                    assert int(len(changes_temp)) == 2
                    if(changes_temp[0] == 'date' and changes_temp[1] in ('on', 'off')):
                        if(changes_temp[1] == 'on'):
                            self._showdate = 1
                            self.settings_view
                        elif(changes_temp[1] == 'off'):
                            self._showdate = 0
                            self.settings_view
                        save_setting(self._showdate)
                        continue
                    else:
                        sys.stderr.write("Invalid Command. Please try again!")
                        continue
                    
                except AssertionError:
                    sys.stderr.write("Cannot interpret input. Please try again!")
                    continue
        return
#-----------------------Class Category--------------------
class Categories: #read category from txt file, when assigning, add numerics for help.
    def __init__(self):
        '''init category'''
        self._category = ['expense',['food',['meal','drink','snacks']],'income',['salary', 'allowance']]
        #make it read from text file.
        return
    
    def valid_cat(self, cat, key):
        '''check validity'''
        if type(cat) not in {list}:
            if cat == key:
                return 1
            else:
                return 0
        else:
            flag = 0
            for item in cat:
                flag = self.valid_cat(item, key)
                if flag == 1:
                    return flag
            return flag
    
    def find_subcategories(self, category, categories):
        '''given functions from TAs <3'''
        def find_subcategories_gen(category, categories, found=False): #returns an address to generator object!
            '''given by TAs''' 
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(category, categories[index+1], found = True)
            else:
                if categories == category or found == True:
                    yield categories
                    
        return list(find_subcategories_gen(category, categories, found = False)) #return the list of selected categories
    
    def view_cat(self, cat, lvl):
        """View categories function"""
        if type(cat) not in {list}:
            print(' ' * 4 * lvl, end='') #print spacing
            print('⇨', end='') #print pointer
            print(cat)
            return
        else:
            for items in cat:
                self.view_cat(items, lvl+1) #recursive call, add level count by 1.
            return


#------------------------Main----------------------------
cat = Categories()
me = Records()
while True:
    Prompt = str(input("Hello, {:s}! what do you want to do (add / view / find / delete / settings / reset / exit)? ".format(me._name))).lower()
    
    if Prompt == 'add': ##Add prompt
        temp_prompt = str(input("What do you want to add (records / cancel)? ")).lower()
        if temp_prompt in ('records', 'record'):
            change=str(input("Add an expense or income record with description and amount: "))
            me.add(change)
        elif temp_prompt == 'cancel':
            print("\ncanceled!\n")
            continue
        else:
            sys.stderr.write("Sorry, this command is invalid. Please try again!\n")
            continue
    elif Prompt == 'view':
        temp_prompt = str(input("What do you want to view (records / categories / cancel)? ")).lower()
        if temp_prompt in ('records', 'record'): ##View records
            if me._showdate == 1:
                me.view_date(me._amount, me._logbook)
            elif me._showdate == 0:
                me.view(me._amount, me._logbook)
            continue
        if temp_prompt in ('categories', 'category'): ##View categories
            print("\nHere are the available categories in your account:\n===================================================")
            cat.view_cat(cat._category, -1)
            continue
        elif temp_prompt == 'cancel':
            print("\ncanceled!\n")
            continue
        else:
            sys.stderr.write("Sorry, this command is invalid. Please try again!\n")
            continue
    elif Prompt == 'find':
        me.find
        continue
    elif Prompt == 'delete':
        me.delete
        continue
    elif Prompt == 'reset': ##Reset prompt
        exit_flag = me.reset
        if exit_flag ==1:
            break
        elif exit_flag == 2:
            continue
    elif Prompt == 'exit':
        exit_flag = me.exit
        if exit_flag==1:
            break
        elif exit_flag==2:
            continue
    elif Prompt in ('settings', 'setting'):
        me.settings_welcome
        continue
    else:
        sys.stderr.write("Sorry, invalid command! Please try again!")
        continue

