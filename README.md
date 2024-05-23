# hagi-bot

## **Overview**

This repository contains scripts detailing the model of the dialogue system "hagi-bot," which was submitted to the [Dialogue System Live Competition 6](https://sites.google.com/view/dslc6/%E3%83%9B%E3%83%BC%E3%83%A0) and passed the preliminary round in first place. It also includes the experimental results conducted with this system.

## **Explanation of Distributed Resources**

This system is a multimodal dialogue system, and it requires the software distributed by the organizers to animate the avatar. Additionally, we will release a local model for text-based response generation via the command line without using the distributed software.

The multimodal model submitted to the competition is available in the [multimodal folder](https://github.com/cl-tohoku/hagi-bot/tree/main/multimodal).

The local model for text-based response generation is available in the [local folder](https://github.com/cl-tohoku/hagi-bot/tree/main/local).

### **Response Generation Module**

In this system, the dialogue state is monitored in a slot-filling format, allowing for the continuous adjustment of prompts according to the situation, which enables the natural development of context-aware discussions.

OpenAI's GPT-4 is used for both response generation and slot-filling. To run this system, the OpenAI API is required. Please replace **`OPENAI_API_KEY`** with your own API key.

### **Prompts**

The content described in the prompts can be found [here](https://github.com/cl-tohoku/hagi-bot/blob/main/local/clients/prompts/system_instructions.py).

### **How to Specify the OpenAI API Key**

1. If specifying in ~/.zshrc:
Add the following to your ~/.zshrc file:
    
    ```arduino
    export OPENAI_API_KEY="[your OpenAI API key]"
    ```
    
2. If specifying directly in the code:
Replace line 35 (the first line of the main function) in [this file](https://github.com/cl-tohoku/hagi-bot/blob/main/local/run.py) with the following:
    
    ```arduino
    openai.api_key = "[your OpenAI API key]"
    ```
    
    ## **Multimodal Model**
    
    This is the multimodal dialogue system submitted to the competition.
    
    It requires the distributed software, so it may not be executable by non-participants. If you wish to run it, please refer to the [local model](https://github.com/cl-tohoku/hagi-bot?tab=readme-ov-file#%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%83%A2%E3%83%87%E3%83%AB).
    
    The entire system is available in the [multimodal folder](https://github.com/cl-tohoku/hagi-bot/blob/main/multimodal).
    
    The scripts for the core of the multimodal model are located in the [hagi_bot folder](https://github.com/cl-tohoku/hagi-bot/blob/main/multimodal/dslc6/hagi_bot).
    
    ### **Execution Method**
    
    For environment setup, please refer to [this guide](https://sites.google.com/view/dslc6/getting-started).
    
    To start all the software necessary for the dialogue system, double-click **`start.bat`** in the [multimodal folder](https://github.com/cl-tohoku/hagi-bot/blob/main/multimodal).
    
    Once all the software has started, follow these steps:
    
    ```bash
    # Clone the repository
    git clone <https://github.com/cl-tohoku/hagi-bot.git>
    cd multimodal/dslc6
    
    # Build the docker image
    docker build dslc6 -t dslc6
    
    # Start the docker container and run the dialogue system
    docker run --add-host="host.docker.internal:host-gateway" --rm -it dslc6
    ```
    
    ## **Local Model**
    
    This command-line dialogue system can be executed in a local environment without the distributed software.
    
    ### **Execution Method**
    
    **Environment**
    
    - Python 3.10
    - openai == 0.28.1
    - tiktoken == 0.5.1
    - timeout_decorator == 0.5.0
    
    ```bash
    # Clone the repository
    git clone <https://github.com/cl-tohoku/hagi-bot.git>
    cd hagi-bot/local
    
    # Install the required libraries
    pip install -r requirements.txt
    
    # Run the model and interact via command-line (--debug allows you to check generation time and slot contents)
    python run.py --stream --main-model gpt-4 --slot-model gpt-4
    ```
    
    ### **Explanation of Command-Line Arguments**
    
    | Command-Line Argument | Description |
    | --- | --- |
    | stream | Changes the generation method |
    | main-model | Specifies the response generation model |
    | slot-model | Specifies the slot model |
    | debug | Checks generation time and slots |
    - **stream**
        - Specifies whether to generate all response sentences at once or to generate them at each delimiter (、。?!…).
        - **`-stream`** off: Generate all at once.
        - **`-stream`** on: Generate at each delimiter.
    - **main-model**
        - Specifies the response generation model.
        - **`-main-model gpt-3.5-turbo`**: Use GPT-3.5-turbo.
        - **`-main-model gpt-4`**: Use GPT-4.
    - **slot-model**
        - Specifies the slot model.
        - **`-slot-model gpt-3.5-turbo`**: Use GPT-3.5-turbo.
        - **`-slot-model gpt-4`**: Use GPT-4.
    - **debug**
        - Enables debug mode to check generation time and slot contents.
        - **`-debug`** off: Display only user and system responses.
        - **`-debug`** on: Display response generation time, slot contents, etc.
        
        ## **Details of Experimental Results**
        
        ### **Experiment Description**
        
        We compared the initial response time when generating responses all at once versus generating them at each delimiter (、。?!…).
        
        ### **Experiment Setup**
        
        - Measurements were taken using the local model.
        - Both the response generation model and the slot model used GPT-4.
        - Response generation time was measured for one dialogue (nine responses).
        
        ### **Experiment Results**
        ![graph](./figure/output.png)
        The average time for generating responses all at once was 13.88 seconds, while the average time for generating responses at each delimiter was 3.22 seconds.
        
        ### **Discussion**
        
        Generating responses at each delimiter was more than 10 seconds faster than generating them all at once. This can be attributed to the fact that response generation time depends on the length of the generated text.
        
        Additionally, the large difference in generation time for the same model is likely due to server connection and congestion conditions. Notably, for the third response, generating it all at once took more than 20 seconds, whereas generating it at each delimiter took only about 2 seconds. This indicates that there were instances of prolonged response generation during the process. When using the multimodal model, generating responses all at once results in longer waiting times for the user. However, by splitting the responses at delimiters, the system can generate and speak responses incrementally, reducing the perceived waiting time for the user.
        
        ## License
        
        The models are distributed under the terms of the [Creative Commons Attribution-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
        
        The source code is licensed MIT.
        
        **Contact**
        
        If you have any questions, please contact Yuto Nakano at nakano.yuto.t2@dc.tohoku.ac.jp or Shinnosuke Nozue at nozue.shinnosuke.q5@dc.tohoku.ac.jp.