### Mailing_bot
<b>You need to use this command to install all dependencies and then run bot:</b>
<pre>pip install -r requirements.txt</pre>

<b>First of all add the bot to the group where you are admin</b>
<b>Then use those commands to continue:</b>
<pre> /moderator <b> to go through "if admin" checking (admin keyboard will appear in bot_chat)</b></pre>
<pre> /delete <b> to delete messages from DB </b></pre>
<pre> /upload <b> this command in bot_chat will start the machine state, so you will be able to add messages to DB </b></pre>
<pre> /cancel <b> to finish the machine state </b></pre>
<pre> /checklist <b> to watch all saved messages from DB </b></pre>
### After someone uses the command /start - his user_id is saving to DB, so admin will be able to choose message from checklist and start mailing by means of 'broadcast' button under every message

### At last, after mailing is finished, mailing loop is creating report.html with report about successful or failed tries with users_id