from cryptopolis.stacking_transaction import main


def lambda_handler(event, context):
    task = event["task"]

    cryptopolis_stacking_contract = "0x8e3cfca4995d2ec53e1001707cd6f3d58a32b334"
    if task == "get-stacking-transaction":
        main(cryptopolis_stacking_contract)
    elif task == "":
        pass
    else:
        pass


def retrieve_all_transactions():
    transactions_chunk_empty = False
    transactions = []
    initial_block = 0
    loop_nb = 1
    while transactions_chunk_empty is False:
        print(f"Loop number {loop_nb}")
        loop_nb += 1
        transactions_chunk = get_transaction_from_block(initial_block)
        print(transactions_chunk.shape)
        transactions.append(transactions_chunk)
        if len(transactions_chunk) <= 2:
            transactions_chunk_empty = True
        initial_block = get_last_block(transactions_chunk)
    return transactions
