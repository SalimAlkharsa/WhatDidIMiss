# What Did I Miss - Slack Bot

Welcome to What Did I Miss, a Slack bot that helps you catch up on important discussions by summarizing old messages in a concise format. With this bot, you can stay informed and quickly get up to speed on the latest updates in your Slack channels.

## How it Works

The application server logs a maximum of 25 messages across 5 channels. When a user mentions the bot followed by a message, the bot will return a short bullet point answer with emphasis on the question. For example, if you ask "@what did I miss, was there anything important from the meeting?" the bot will provide a summary that focuses more on meeting tasks.

The summary AI is powered by Cohere's summary endpoint, which utilizes advanced natural language processing techniques. If there is not enough text to summarize or any other error occurs, the bot will message the user, informing them that there isn't enough text to generate a summary.

## Running your own version of it

If you would like to try out the bot or contribute to its development, follow the instructions below:

1. Set the following environment variables:
   - `COHERE_API_KEY`: Obtain this key from [Cohere](https://cohere.com) to use their summary endpoint.
   - `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`: Follow [Slack's instructions](https://api.slack.com/authentication/token-types) to obtain these keys.

2. Deployment on Heroku (for production):
   - Deploy the code to Heroku or your preferred hosting platform.
   - Configure the environment variables mentioned above.
   - Make sure to follow Cohere's policy on API usage in production

3. Development environment using ngrok:
   - Install [ngrok](https://ngrok.com) to expose your local server to the internet.
   - Follow the instructions found in the [Slack Bolt Python tutorial](https://slack.dev/bolt-python/tutorial/getting-started) to set up your development environment.

If you have any questions about setting up the project or general inquiries, please raise an issue, and I'll respond as soon as possible.

## Known Issues & Bugs

- The messages and channels are implemented as a FIFO (First-In, First-Out) queue. However, the current implementation clears the first input channel once all five channels are filled. It would be more ideal to remove the last or least used channel instead.
- When the 25-message capacity is reached in a channel, the channel is deleted from the bot's data. It would be better to implement a FIFO queue for the messages within a channel.
- The implementation of the mention handling sometimes triggers the bot to listen twice, causing it to reply twice.

## Plans Moving Forward

I will continue working on this project sporadically to address the above bugs and issues. Additionally, I am exploring training my own NLP classification algorithm to better map the focus of the summary. By improving the classification, the user experience can be enhanced, as the summary generation parameters can be better tuned. Currently, the user message following the mention is added as a command parameter to the Cohere summary endpoint, but I am interested in exploring if performance can be improved by altering the model generation parameters.

Feel free to contribute to this project by opening pull requests or suggesting improvements. Your contributions are greatly appreciated!

