import openai as ai
import panel as pn

ai.api_key="YOUR API KEY HERE"
model = "gpt-4o-mini"

#This function will receive the different messages in the conversation,
#and call OpenAI passing the full conversation.
def continue_conversation(messages, temperature=0):
    response = ai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def add_prompts_conversation(_):
    #Get the value introduced by the user
    prompt = client_prompt.value_input
    client_prompt.value = ''

    #Append to the context the User prompt.
    context.append({'role':'user', 'content':f"{prompt}"})

    #Get the response.
    response = continue_conversation(context)

    #Add the response to the context.
    context.append({'role':'assistant', 'content':f"{response}"})

    #Update the panels to show the conversation.
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600)))

    return pn.Column(*panels)

context = [ {'role':'system', 'content':"""
You work collecting orders at a sandwhich shop called Jake's sandwiches.

First welcome the customer then collect the order.

Instructions:
-Collect the entire order by first asking about bread, then meat, then cheese, then veggies, and finally toppings. Only items from the menu are allowed.
-Summarize the order including the total price
-Ask if there are any final changes
-Give the customer and tell them to wait to be called

Menu:
Bread:
-whole wheat
-white
-hard roll
-wrap
-gluten free bun

Meat:
-Turkey
-Roast Beef
-Ham

Cheese:
-American
-Swiss
-Provolone

Veggies:
-Lettuce
-Tomato
-Onions
-Bannana Peppers

Toppings:
-Mayo
-Mustard
-Horseraddish Sauce
-Oil and Vinegar

All sandwhiches cast $5 except if they have a gluten free bun, then they cost $7.

"""} ]

pn.extension()

panels = []

client_prompt = pn.widgets.TextInput(value="Hi",placeholder='Enter text here:')
button_conversation = pn.widgets.Button(name="send")

interactive_conversation = pn.bind(add_prompts_conversation, button_conversation)

dashboard = pn.Column(
    client_prompt,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indictor=True),
)

pn.serve(dashboard)

