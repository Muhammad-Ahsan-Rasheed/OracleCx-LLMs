import openai

# OpenAI API Key
openai.api_key = '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'

table = """### Oracle 11gR2 SQL tables, with their properties:
           #
           # CHATGPT_SALE_MASTER(BUILDING: TOWER A, UNIT_CODE, UNIT_NUMBER, GROSS_AREA, BALCONY_AREA, SALE_VALUE, OFFER_NO, BLOCK_DATE, RESERVE_NO, BOOKING_DATE, BOOKING_NO, UNIT_STATUS, AGENT_NAME, BROKER_NAME, CUSTOMER_NAME, CUSTOMER_ID)
           # 
           """


def get_query(message, max_token):
    """
    Call the OpenAI API to generate a response to a given prompt.
    Parameters:
        - prompt (str): The message to generate a response for.
    Returns:
        - str: The generated response from the OpenAI API.
    """
    prompt = f"""
                {table}
                # Generate a query from a given prompt strictly following the table structure
                #
                ### prompt: Total Sale value -> completion: select Sum(Sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved');
                ### prompt: Total Pre booked -> completion: select count(*) from chatgpt_sale_master where  unit_status IN ('Booked');
                ### prompt: Total Reserved -> completion: select count(*) from chatgpt_sale_master where  unit_status IN ('Reserved');
                ### prompt: Total sale value of the Tower A -> completion: select Sum(Sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and buidling = 'TOWER A';
                ### prompt: Total sale value of the Tower B -> completion: select Sum(Sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and buidling = 'TOWER B';
                ### prompt: Last 10 days Total sale value -> completion: select Sum(Sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between sysdate -10  and sysdate ;
                ### prompt: Last month Total sale value -> completion: select Sum(Sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between '01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY') and last_day(add_months(sysdate,-1)) ;
                ### prompt: Total sale value in Aug 2022 -> completion: select sum(sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between '01-AUG-2022' and last_day('01-AUG-2022') ;
                ### prompt: Last 10 days Average sale value -> completion: select Sum(Sale_value)/10  from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between sysdate -10  and sysdate ;
                ### prompt: Last month Average sale value -> completion: select Sum(Sale_value)/round(last_day(add_months(sysdate,-1)) - to_date('01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY'),'DD-MON-YYYY'))\nfrom chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between '01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY') and last_day(add_months(sysdate,-1)) ;\n
                ### prompt: Average sale value in august 2022-> completion: select sum(sale_value)/(last_day('01-AUG-2022') - to_date('01-AUG-2022','DD-MON-YYYY')) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between '01-AUG-2022' and last_day('01-AUG-2022') ;
                ### prompt: Last 10 days Total Pre booked -> completion: select Count(*) from chatgpt_sale_master where  unit_status IN ('Booked') and booking_date between sysdate -10  and sysdate ;
                ### prompt: Last month Total Pre booked -> completion: select Count(*) from chatgpt_sale_master where  unit_status IN ('Booked') and booking_date between '01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY') and last_day(add_months(sysdate,-1)) ;
                ### prompt: Total Pre booked in Aug-> completion: select count(*) from chatgpt_sale_master where  unit_status IN ('Booked') and booking_date between '01-AUG-2022' and last_day('01-AUG-2022') ;
                ### prompt: Last 10 days Average Pre booked -> completion: select count(*)/10  from chatgpt_sale_master where  unit_status IN ('Booked') and booking_date between sysdate -10  and sysdate ;
                ### prompt: Last month Average Pre booked -> completion: select count(*)/round(last_day(add_months(sysdate,-1)) - to_date('01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY'),'DD-MON-YYYY'))\nfrom chatgpt_sale_master where  unit_status IN ('Booked') and booking_date between '01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY') and last_day(add_months(sysdate,-1)) ;
                ### prompt: Specific month Average Pre booked -> completion: select count(*)/(last_day('01-AUG-2022') - to_date('01-AUG-2022','DD-MON-YYYY')) from chatgpt_sale_master where  unit_status IN ('Booked') and booking_date between '01-AUG-2022' and last_day('01-AUG-2022') ;
                ### prompt: Last 10 days Total Reserved -> completion: select Count(*) from chatgpt_sale_master where  unit_status IN ('Reserved') and booking_date between sysdate -10  and sysdate ;
                ### prompt: Last month Total Reserved -> completion: select Count(*) from chatgpt_sale_master where  unit_status IN ('Reserved') and booking_date between '01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY') and last_day(add_months(sysdate,-1)) ;
                ### prompt: Specific month Total Reserved -> completion: select count(*) from chatgpt_sale_master where  unit_status IN ('Reserved') and booking_date between '01-AUG-2022' and last_day('01-AUG-2022') ;
                ### prompt: View units purchased by customer -> select q.buidling, q.unit_code,q.booking_date, a.unit_specs_name from chatgpt_sale_master q left join chatgpt_unit_master a on a.unit_code = q.unit_code where unit_status IN ('Booked','Reserved') and lower(customer_name) like ' %arthur colibao%'; 
                ### prompt: {message} -> completion: """

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0.9,
        max_tokens=max_token,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        stop=["#", ";"]
    )

    return response["choices"][0]["text"]


def turn_into_sentence(data, question, query, max_token):
    """
    Get the data and turn it into a sentence.
    Parameters:
        - data (str): The data to convert into a sentence.
    Returns:
        - str: The converted sentence.
    """
    try:
        prompt = f"Suppose you're my assistant. Turn given real estate data into sentence and reply " \
                 f"to me strictly following the question. If data is empty just say No Record Found\n" \
                 f"Query: {query}\n" \
                 f"Question: {question}\n" \
                 f"Data: {data}\n" \
                 f"Answer:"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=max_token,
        )

        return response["choices"][0]["text"]
    except Exception as e:
        print(e)
        return "Data Size is too large."
