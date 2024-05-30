from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import CassandraChatMessageHistory
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pyprojroot import here
import toml

# NOTE: location of this has changed, see below link:
# https://docs.datastax.com/en/astra-db-serverless/drivers/secure-connect-bundle.html
cloud_config= {
  'secure_connect_bundle': 'secure-connect-choose-your-own-adventure.zip'
}

secrets = toml.load(here(".secrets.toml"))
CLIENT_SECRET = secrets["datastax"]["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_KEYSPACE = secrets["datastax"]["ASTRA_DB_KEYSPACE"]
OPENAI_API_KEY = secrets["openai"]["OPENAI_API_KEY"]
auth_provider = PlainTextAuthProvider("token", CLIENT_SECRET)
# From below link:
# https://docs.datastax.com/en/astra-db-serverless/drivers/python-quickstart.html
session = Cluster(
    cloud=cloud_config,
    auth_provider=auth_provider,
).connect()

message_history = CassandraChatMessageHistory(
    session_id="anything",
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_seconds=3600
)
message_history.clear()
cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

template = """
You are the guide of a mystical journey through the Jubilee Jungle. A
player-controlled traveller seeks the lost Crown of Hope. You must navigate the
player through challenges, providing choices, and consequences, dynamically
adapting the tale based on the traveller's inputs. Your goal is to create a
branching narrative experience where each of the traveller's choices leads to a
new path, ultimately determining the traveller's fate. 

Here are some rules to follow:
1. Always wait for the traveller to respond with their input before making any
choices. Never provide the player's input yourself. This is most important.
2. Ask the player to provide a name, gender and race.
3. Ask the player to choose some weapons that will be used later in the game.
4. Have a few paths that lead to success. 
5. Have some paths that lead to death.
6. Whether or not the game results in success or death, the response must
include the text "The End...", I will search for this text to end the game.

Here is the chat history, use this to understand what to say next:
{chat_history}

Below is the input from the user playing the game. Allow the user to provide
this text, do not provide it yourself. Double check to ensure that you are not
providing the human input yourself, it must come from the person playing the
game: {human_input}

Use the below format to provide your response. Ensure this is the only section
where you provide your response:
Guide:

"""
prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)
oai_llm = OpenAI(openai_api_key=OPENAI_API_KEY)

llm_chain = LLMChain(
    llm=oai_llm,
    prompt=prompt,
    memory=cass_buff_memory
) # Deprecation warning: Use RunnableSequence, e.g., `prompt | llm` instead.
choice = "Begin the adventure."
while True:
    response = llm_chain.predict(human_input=choice)
    print(response.strip())
    if "The End..." in response:
        break
    choice = input("Your reply: ")
