# reddit-search-engine
A basic self post only search engine for the subreddit /r/Gunners, implemented using Flask and Bootstrap.
##Usage :
*Clone the repository
```
cd
git clone https://github.com/ambardhesi/reddit-search-engine.git
```
*Create the database
To do this, you must create two directories `crawledUrls` and `indexes` in the same folder.
Now, run the following command
```
python crawler.py --start_url https://reddit.com/r/Gunners --storage_dir crawledUrls
```
This command will download data from /r/gunners subreddit to the `crawledUrls` directory. It will keep running till stopped by the user.
After this, run the following command
```
python indexer.py --stored_files_dir crawledUrls --storage_dir indexes
```
This command will create the indexes from `crawledUrls` directory and save them in the `indexes` directory.

Finally, run the command to set up the server as follows :
```
python webapp_ui.py
```
and open the link http://127.0.0.1:5000/ in your browser. 
![alt text](screenshots/Image1.png)
![alt text](screenshots/Image2.png)
