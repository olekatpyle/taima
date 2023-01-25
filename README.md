         *##########*
      *################*
     *##################*
    *####################*
    *####################*
     *##################*
      *###*########*###*
       *##############*
      *################*
      *################*
       *##############*
          *########*

# PYMEON LEE ORG
presents

</br>

## Taimā (ˈta͜imɐ) - [taima]

##### CLI timer application written in python3.10.0 utilizing sqlite3 to track your times locally, you spent at your computer working hard.

---

</br>

The purpose of this application is to simply track your working times locally and utilizing a sqlite3 database to save all your times. This is work in progress, current version is <b>1.2.1</b>. See the feature section to see all functionalities currently supported.

</br>

---

## Installation and Usage of taima~1.x.x

### Prerequisites
* sqlite3 3.7.15 or higher (see Python Docs)
* python3.10 installed (development version)
  * other python versions will be tested soon

For version 1 of this application, you only need to clone the repository to your local machine. In order to allow for system wide program calls for the user, run the [`setup.sh`](./setup.sh) to set the PATH variable inside your `.bashrc`. You will need to either restart your terminal or run `source ~/.bashrc` in your shell to make this change take effect. Any other shell is currently not part of the setup process, but should easily be adjusted manually, since only a PATH variable for the taima executable needs to be added. 
After that you are good to go to initiate a database in any working directory with `taima init` and run the program inside of it afterwards, as long as permission is granted for the directory by the system. 
Future updates can be obtained with a `git pull origin main` or downloading the updated files.   

---
<b>Important Note</b>

This application is published under the GNU General Public Licence v3.0, thus is to be seen as free software. For more information visit https://www.gnu.org/licenses/gpl-3.0.en.html 
or see the attached [LICENSE](./LICENSE)
> Free software is a matter of liberty, not price.
> To understand the concept, you should think of free as
> in free speech, not as in free beer. 
>
> *Richard Stallman*
---
</br>

### Features in taima1.x.x

<b>Taimā [taima] v.1.x.x</b> features the most primitive funtionalities you could expect a timer application to have. These are: 

</br>

Creating the database file *workload.db* for sqlite3 with a single table:

```sql
CREATE TABLE workload(task_ TEXT NOT NULL, 
                      date_ DATE NOT NULL, 
                      times_ TEXT NOT NULL, 
                      total_ INTEGER NOT NULL);

INSERT INTO workload VALUES('hard work', 
                            'Feb-21-1848', 
                            '{"06:00:00":"18:00:00"}', 
                            720);

```

| task       | date      | times     | total    |
|:-----------|:----------|:----------|:---------| 
|hard work   | Feb-21-1848|{"06:00:00":"18:00:00"}|720

</br>
Running the program in an infinity loop keeping track of all relevant data:

For the actual timer the application runs in an infinitiy loop that can be exited through user input.
Inside the loop, the user is prompted for a name for the task or to exit out of the program typing in the keyword <b>*exit*</b>. After creation of a task, the user may start the timer with the keyword <b>*start*</b> or finish work typing <b>*finish*</b>. 
Once the timer session is invoked by <b>*start*</b>, only the <b>*stop*</b> keyword will terminate the loop, update the database with the calculated time for the current task and bring the user back to the choice of either finish work, or continue with another timer session on the current task. 
The <b>*finish*</b> keyword will break out of the timer session loop for the current task and again, prompt the user for a taskname or <b>*exit*</b>, to quit the program. At this point, the user may define a new task by typing in a new name, however the user may continue work on a task by retyping the name of an already defined task. Notice though, that if you work on the same task on multiple days, the database has an individual row per date for this task. This may or may not be relevant for future features.

With <b>taima1.1.0</b> and <b>taima1.2.0</b>, the core functionalities have been completed, to form a functional and versatile software. The addition of the [`argumentHandler`](./src/taima) gives access to the functionalities `init`, `view` and `clean` from the command line interface. 
Calling the program with `taima init`, the database is being setup in a .taima directory within the current working directory(Similiar to a `git init`). Once the program is initialized in the working directory, the program can simply be run with typing `taima` in the command line, starting the already described main loop. However, the program can be started with `taima -t "task"`, in order to specify a task the user wishes to start a timer session on. In that case the initial prompt of typing in a taskname gets skipped and a timer session is entered directly.
To get an overview of your working times, the program features the [`createView`](src/view.py) function, that can be invoked with the `taima view [option]` program call. Passing an additional option, a view based on the passed option gets created and displayed in the terminal. The user may choose between the following options:
* `-td | --today` gives an overview of todays tasks and worktimes
* `-t | --task "task"` gives an overview of the worktimes on the specified task
* `-y | --year "YYYY"` gives an overview of tasks and worktimes in the specified year
* `-m | --month "MM"`  gives an overview of tasks and worktimes in the specified month
* `-d | --date "YYYY-MM-DD"` gives an overview of the tasks and worktimes recorded on specified date
* `-a | --all` displays all recorded tasks and worktimes that are currently in the database

NOTE: When specifying any sort of month, year or date, it is important to keep the correct format as seen above. Currently there is no pattern match like mechanism to accept different formats of dates. However, this might be added in the future.

Lastly the user may run `taima clean [option]`, to perform cleaning tasks on the database defined in the [`cleanDB`](./src/clean.py). Currently supported options are: 
* `-a | --all` to remove every entry in the database
* `-t | --task "task"` to only remove entries for the specified task.
</br>

###### The [CHANGELOG.md](./docs/CHANGE_LOG.md) keeps track of all changes made between different versions, and gives little explanation on some decisions during development. Have a look.

---
### Planned features for taima1.3.0 and announcement of taima2.0.0

<b>taima1.3.0</b>
* Implementation of Arguement Parser to allow the following program calls
  * ~~<b>taima</b> : default program call~~
  * ~~<b>taima [taskname]</b> : starting the timer directly on the specified task, skipping the initial configuration~~
  * ~~<b>taima view [option]</b> : functionality to get a specific overview of the workload data, specified by an arguement 'option'. Depending on the specified arguement a specific view gets printed to show all work times~~
  * <b>taima convert [filetype]</b> : functionality, to convert specified entries into a file format, the first filetype this feature will be developed being a simple .txt file
  * ~~<b> taima clean [option] : functionality to clean the database from specified entries</b>~~

<b>taima2.0.0 planned features</b>
* additions to [`setup.sh`](./setup.sh), in order to check the used shell and configure the hook accordingly 
* better keyboard navigation, preparing the project for a future tmux integration
* more appealing display of views, making use of the keyboard navigation
* program cache to enable command history and future tab completion
* Database archive, a single database that stores entries from all other existing databases, as sort of backup database that works in combination with the `cleanDB` function, to not fully delete an entry
* convert to csv and pdf
 
## Far-future releases features

* better system integration for easier setup
* portability to other os'es
* tmux integration
* gui version

---

Any form of contribution, ideas and criticism is more than welcomed. Best wishes,

Pymeon Lee Org



