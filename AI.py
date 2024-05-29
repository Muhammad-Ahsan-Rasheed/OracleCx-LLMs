from flask import url_for, redirect
import openai

# OpenAI API Key
openai.api_key = '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'

table = """### Table_Name(Column_Name: sample Column_Value, Column_Name: sample Column_Value)
           # 
           # CHATGPT_BOOKING_FORM(NUMBER: 422, BOOKING_FORM_STATUS: Booking Form Not Attached / Booking Form Attached)
           # CHATGPT_BROKER_MASTER(BROKER_REGISTED_DATE: 24-JUN-22,	BROKER_ID: 188, CREATED_ON: 6/24/2022 9:58,	BROKER_NAME: Milestone Home Real Estate Brokers, TELEPHONE: 9714 4516355, EMAIL: makhan@mshre.ae, MOBILE: 971585765338, AGENT: 1, ORG_NAME: FAKHRUDDIN PROPERTIES DEVELOPMENT LIMITED, IS_ACTIVE: 0/1, IS_CONFIRMED_BY: 5236, IS_VERIFIED_BY: 5250)
           # CHATGPT_CUSTOMER_BAL(CUSTOMER_ID: 422, CUSTOMER_NAME: Vivek Jadon, UNITID:	892, UNIT_CODE: MGT1-FL22-2203, SALE_VALUE: 1,000,000.00, OFFER_NO: 791, CINVOICENO: RES-422, RESERVE_NO: 431, DOC_DATE: 16-Aug-22, DOC_TYPE: ERES / INSTALLMENT, INV_AMT: 20,000.00, INV_BALANCE: (invoice amount - paid = invoice balance) 19,500.00, UNASSIGNED: 1,000, RESERVE_DATE: 16-Aug-22, BOOKING_DATE: 9-Nov-22, OUTSTANDING_DAYS: 5, PDC: 1,000.00)
           # CHATGPT_CUSTOMER_CONTACT(CUSTOMER_CREATED_ON: 23-Feb-2023, CUSTOMER_ID: 422, CTYPE: Person / Org, CUSTOMER_NAME: Vivek Jadon, FIRST_NAME: Vivek, LAST_NAME: Jadon, CONTACT_TYPE_NAME: EMAIL / MOBILE, VALUE: info@gmail.com / +971556003992, IS_DISABLED: 0 / 1, IS_PRIMARY: 0 / 1)
           # CHATGPT_CUSTOMER_MASTER(CUSTOMER_ID: 422, CTYPE: Person, CUSTOMER_NAME: Vivek Jadon, FIRST_NAME: Vivek , LAST_NAME: Jadon, PASSPORT_NO: Z123456789, PASSPORT_EXPIRY_DATE: 23-FEB-2028, VISA_EXPIRY_DATE: 23-FEB-2024, DOB:	23-Feb-1984, COUNTRY_ID: 52, NATIONALITY)
           # CHATGPT_PRA( ID: 63, OFFER_NO: 422, CUSTOMER_NAME: Vivek Jadon, RESERVE_DATE: 7-Apr-22, CLIENT_SIGN_DATE: 7-Apr-22, MGMT_SIGN_DATE: 7-Apr-22, CLIENT_HANDOVER_DATE: 7-Apr-22, PRA_STATUS: SIGNED AND FILED, UNIT_STATUS: Reserved, AGENT_ID: 52, ORG_ID: 31, UNIT_CODE: MGT2-FL22-2203, STATUSDT, USER_INFO_ID: 5122, CREATED_BY: 5213)
           # CHATGPT_UNIT_MASTER(BUILDING: TOWER A / TOWER B, UNIT_CODE: MGT2-FL23-2301, UNIT_NUMBER: 2301, GROSS_AREA: 1000.56, BALCONY_AREA: 52.36, PRICE_VALUE: 2,000,000.00, UNIT_SPECS_NAME: 1 BHK / STUDIO / 2 BHK, UNIT_TYPE_NAME: TYPE 1 / TYPE A, UNIT_VIEW_NAME: Barsha South View, UNIT_OPEN_FOR_SALE: YES / NO)
           # CHATGPT_SALE_MASTER(BUILDING: TOWER A / TOWER B, UNIT_CODE: MGT1-FL22-2201, UNIT_NUMBER: 2313, GROSS_AREA: 3242.34, BALCONY_AREA: 42.5, SALE_VALUE: 525000, OFFER_NO: 430, BLOCK_DATE: 15-Aug-22, RESERVE_NO: 92, BOOKING_DATE: 22-Aug-22, BOOKING_NO: 117, UNIT_STATUS: Booked, AGENT_NAME: Vandana, BROKER_NAME: PHIRDOS STAR PROPERTY, CUSTOMER_NAME: Arthur Colibao, CUSTOMER_ID: 434)
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

    prompt = f"""### Oracle 11gR2 SQL tables, with their properties, data types and examples(if applicable):
                #
                {table}
                #
                ### Try to generate the sql query according to prompt. You can adjust the query as needed to include any additional criteria or to include other attributes from the table.
                ### prompt: All Unit Sold on Today ->, completion: select building, unit_code , customer_name from chatgpt_sale_master where unit_status IN ('Booked','Reserved') and trunc(booking_date) = to_date('03-03-23','DD-MM-YY');
                ### prompt: All Units Sold for Tower A ->, completion: select unit_code , customer_name,booking_date from chatgpt_sale_master where unit_status IN ('Booked','Reserved') and building = 'TOWER A'; 
                ### prompt: All units Sold by PHIRDOS STAR PROPERTY ->, completion: select building, unit_code , customer_name,booking_date from chatgpt_sale_master where unit_status IN ('Booked','Reserved') and lower(broker_name) like '%phirdos star property%';
                ### prompt: how many customer purchased 1 bedroom ->, completion: select q.building, q.unit_code,q.booking_date,q.customer_name,b.nationality  from chatgpt_sale_master q left join chatgpt_unit_master a on a.unit_code = q.unit_code left join chatgpt_customer_master b on b.customer_id = q.customer_id where q.unit_status IN ('Booked','Reserved') and  a.unit_specs_name= '1 BHK';
                ### prompt: Total sale value of the Tower A ->, completion: select Sum(Sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and building = 'TOWER A';
                ### prompt: Last month Total sale value ->, completion: select Sum(Sale_value) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between '01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY') and last_day(add_months(sysdate,-1));
                ### prompt: Last month Average sale value ->, completion: select Sum(Sale_value)/round(last_day(add_months(sysdate,-1)) - to_date('01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY'),'DD-MON-YYYY')) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') and booking_date between '01-'||to_char(last_day(add_months(sysdate,-1)),'MON-YYYY') and last_day(add_months(sysdate,-1));
                ### prompt: Top 5 agent who sold the units in last 10 days ->, completion: select * from (select agent_name , count(*)  from chatgpt_sale_master where agent_name is not null and unit_status IN ('Booked','Reserved') and BLOCK_DATE between sysdate -10  and sysdate group by agent_name order by count(*) desc ) where ROWNUM <= 5;
                ### prompt: Mulitple Broker with same agent ->, completion: select broker_name,agent_name from chatgpt_sale_master where broker_name is not null and agent_name in (select agent_name from (select agent_name, count(*) from (select agent_name,broker_name from chatgpt_sale_master where broker_name is not null group by agent_name,broker_name ) group by agent_name having count(*) > 1)) group by agent_name,broker_name order by agent_name;
                ### prompt: Customer brought more then 5 units ->, completion: select * from (select customer_name, count(*) from chatgpt_sale_master where  unit_status IN ('Booked','Reserved') group by customer_name order by count(*) desc ) where ROWNUM <= 5;
                ### prompt: tell us all Organiazation list ->, completion: select customer_name from chatgpt_customer_master where ctype = 'ORG';
                ### prompt: View Customers who passport expired are from india ->, completion: select customer_name from chatgpt_customer_master where nationality like '%India%' and passport_expiry_date < sysdate;
                ### prompt: When Management signed for the unit ->, completion: select mgmt_sign_date from chatgpt_pra where unit_code = 'MG1-FL1-101';
                ### prompt: How many Units are Management signed by last 10 days ->, completion: select count(*) from chatgpt_pra where mgmt_sign_date is not null and mgmt_sign_date BETWEEN sysdate - 10 and sysdate;
                ### prompt: How many units are pending for Client Sign ->, completion: select count(*) from chatgpt_pra where client_sign_date is null;
                ### prompt: Top 5 Indian customers Needs to pay most ->, completion: select * from (select x.customer_name , sum(x.inv_balance) from chatgpt_customer_bal x left join chatgpt_customer_master y on y.customer_id = x.customer_id where y.nationality like '%India%' and x.doc_type IN ('ERES','ERES Difference','ERES Difference 1','Home Automation','INSTALLMENT') group by x.customer_name having sum(x.inv_balance) > 0 order by sum(inv_balance) desc) where rownum <= 5;
                ### prompt: month wise top agent for the last 6 months ->, "select * from (select agent_name , to_Char(booking_date,'MON-YYYY') as month ,count(*) as sold from chatgpt_sale_master where agent_name is not null and unit_status IN ('Booked','Reserved')group by agent_name,to_Char(booking_date,'MON-YYYY') ) x where x.month||x.sold IN ( select month||sold from (select max(sold) as sold,month from (select agent_name , to_Char(booking_date,'MON-YYYY') as month ,count(*) as sold from chatgpt_sale_master where agent_name is not null and unit_status IN ('Booked','Reserved') group by agent_name,to_Char(booking_date,'MON-YYYY') order by count(*) desc ) group by month));
                ### prompt: {message} ->, completion: """

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=max_token,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )

    return response["choices"][0]["text"]

def turn_into_table(data, question, query, max_token):
    """
    Get the data and turn it into a table.
    Parameters:
        - data (str): The data to convert into a table.
    Returns:
        - str: The converted table.
    """
    try:
        conversation = [{"role": "system", "content": f"Suppose you're my assistant. Turn given real estate data into sentence and reply to me strictly following the table properties. If data is empty just say No Record Found\n"}]
        conversation.append({"role": "user", "content": f"Query: {query}\nQuestion: {question}\nData: {data}\nAnswer:"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.9,
            max_tokens=max_token,
        )

        return str(response['choices'][0]['message']['content'])

    except Exception as e:
        print(e)
        return "Data Size is too large."


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
                 f"to me strictly following the table properties. If data is empty just say No Record Found\n" \
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
        return "Data Size is too large."
