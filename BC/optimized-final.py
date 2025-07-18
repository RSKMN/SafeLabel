import py7zr
import os
import ipfshttpclient
from web3 import Web3
from web3.exceptions import Web3RPCError
import requests

# Global variables
client = ipfshttpclient.connect()
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/PROJECT_ID'))
my_address = 'PROJECT_ID'
private_key = 'PRIVATE_KEY'
claims_dict = {}
file_dict = {}

contract_interface = {
    "abi": [  # Your ABI goes here
        # ...
    ],
    "bin": "6080604052348015600e575f80fd5b50610d118061001c5f395ff3fe608060405234801561000f575f80fd5b506004361061004a575f3560e01c806322453b3a1461004e5780638c9e1f3c1461006a578063a6acce351461009d578063f761d008146100d0575b5f80fd5b6100686004803603810190610063919061078a565b6100ec565b005b610084600480360381019061007f919061078a565b6101f3565b604051610094949392919061088a565b60405180910390f35b6100b760048036038101906100b2919061078a565b6103d5565b6040516100c7949392919061088a565b60405180910390f35b6100ea60048036038101906100e591906108db565b610550565b005b5f80826040516100fc919061098b565b90815260200160405180910390205f018054610117906109ce565b905011610159576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161015090610a48565b60405180910390fd5b60015f8260405161016a919061098b565b90815260200160405180910390206002015f6101000a81548160ff021916908315150217905550335f826040516101a1919061098b565b908152602001604051809103902060020160016101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b6060805f805f8086604051610208919061098b565b90815260200160405180910390206040518060800160405290815f82018054610230906109ce565b80601f016020809104026020016040519081016040528092919081815260200182805461025c906109ce565b80156102a75780601f1061027e576101008083540402835291602001916102a7565b820191905f5260205f20905b81548152906001019060200180831161028a57829003601f168201915b505050505081526020016001820180546102c0906109ce565b80601f01602080910402602001604051908101604052809291908181526020018280546102ec906109ce565b80156103375780601f1061030e57610100808354040283529160200191610337565b820191905f5260205f20905b81548152906001019060200180831161031a57829003601f168201915b50505050508152602001600282015f9054906101000a900460ff161515151581526020016002820160019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815250509050805f01518160200151826040015183606001519450945094509450509193509193565b5f818051602081018201805184825260208301602085012081835280955050505050505f915090508 05f01805461040b906109ce565b80601f0160208091040260200160405190810160405280929190818152602001828054610437906109ce565b80156104825780601f1061045957610100808354040283529160200191610482565b820191905f5260205f20905b81548152906001019060200180831161046557829003601f168201915b505050505090806001018054610497906109ce565b80601f01602080910402602001604051908101604052809291908181526020018280546104c3906109ce565b801561050e5780601f106104e55761010080835404028352916020019161050e565b820191905f5260205f20905b8154815290600101906020018083116104f157829003601f168201915b505050505090806002015f9054906101000a900460ff16908060020160019054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905084565b60405180608001604052808381526020018281526020015f151581526020015f73ffffffffffffffffffffffffffffffffffffffff168152505f83604051610598919061098b565b90815260200160405180910390205f820151815f0190816105b99190610c0c565b5060208201518160010190816105cf9190610c0c565b506040820151816002015f6101000a81548160ff02191690831515021790555060608201518160020160016101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055509050505050565b5f604051905090565b5f80fd5b5f80fd5b5f80fd5b5f80fd5b5f601f19601f8301169050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b61069c82610656565b810181811067ffffffffffffffff821117156106bb576106ba610666565b5b80604052505050565b5f6106cd61063d565b90506106d98282610693565b919050565b5f67ffffffffffffffff8211156106f8576106f7610666565b5b61070182610656565b9050602081019050919050565b828183375f83830152505050565b5f61072e610729846106de565b6106c4565b90508281526020810184848401111561074a57610749610652565b5b61075584828561070e565b509392505050565b5f82601f8301126107715761077061064e565b5b813561078184826020860161071c565b91505092915050565b5f6020828403121561079f5761079e610646565b5b5f82013567ffffffffffffffff8111156107bc576107bb61064a565b5b6107c88482850161075d565b91505092915050565b5f819050919050565b5f819050919050565b610b10610b0b610b0684610ae4565b610aed565b610ae4565b9050919050565b5f819050919050565b610b2983610af6565b610b3d610b3582610b17565b848454610a93565b825550505050565b5f90565b610b51610b45565b610b5c818484610b20565b505050565b5b81811015610b7f57610b745f82610b49565b600181019050610b62565b5050565b601f821115610bc457610b9581610a66565b610b9e84610a78565b81016020851015610bad578190505b610bc1610bb985610a78565b830182610b61565b50505b505050565b5f82821c905092915050565b5f610be45f1984600802610bc9565b1980831691505092915050565b5f610bfc8383610bd5565b9150826002028217905092915050565b610c15826107 d1565b67ffffffffffffffff811115610c2e57610c2d610666565b5b610c3882546109ce565b610c43828285610b83565b5f60209050601f831160018114610c74575f8415610c62578287015190505b610c6c8582610bf1565b865550610cd3565b601f198416610c8286610a66565b5f5b82811015610ca957848901518255600182019150602085019450602081019050610c84565b86831015610cc65784890151610cc2601f891682610bd5565b8355505b6001600288020188555050505b50505050505056fea2646970667358221220f4cbe41f4ad95534a2e58dce2c6aa707f52a20bb28f9d8d3224d05a60e7ce6a864736f6c634300081a0033"
}

def compress_file(ip_pth, op_pth):
    with py7zr.SevenZipFile(op_pth, 'w') as archive:
        archive.write(ip_pth, os.path.basename(ip_pth))
    print(f"Compressed file is saved to : {op_pth}")

def upload_to_ipfs(file_path):
    if file_path in file_dict:
        return file_dict[file_path]
    else:
        with ipfshttpclient.connect() as client:
            result = client.add(file_path)
        file_dict[file_path] = result['Hash']
        return result['Hash']

def get_nonce():
    return w3.eth.get_transaction_count(my_address)

def add_content(cid, description, contract_instance):
    gas_price = w3.to_wei('40', 'gwei')
    nonce = get_nonce()
    tx = contract_instance.functions.addContent(cid, description).build_transaction({
        'from': my_address,
        'nonce': nonce,
        'gas': 305644,
        'gasPrice': gas_price
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Content metadata added to blockchain. Transaction hash:", tx_hash.hex())

def verify_content(cid, contract_instance):
    gas_price = w3.to_wei('40', 'gwei')
    nonce = get_nonce()
    tx = contract_instance.functions.verifyContent(cid).build_transaction({
        'from': my_address,
        'nonce': nonce,
        'gas': 305644,
        'gasPrice': gas_price
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Content verified on blockchain. Transaction hash:", tx_hash.hex())

def retrieve_file_from_ipfs(cid):
    gateways = [
        'https://ipfs.io/ipfs/',
        'https://gateway.pinata.cloud/ipfs/',
        'https://dweb.link/ipfs/',
        'https://infura-ipfs.io/ipfs/',
        'http://localhost:8080/ipfs/'
    ]
    for gateway in gateways:
        try:
            response = requests.get(gateway + cid, timeout=60)
            if response.status_code == 200:
                return response.content
            else:
                print(f'Error retrieving file from {gateway}: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'An error occurred while accessing {gateway}: {str(e)}')
    raise Exception('Failed to retrieve file from all gateways.')

def add_claim(claim_text):
    if claim_text in claims_dict:
        return claims_dict[claim_text]
    else:
        result = client.add_str(claim_text)
        claims_dict[claim_text] = result  # This is the CID
        return result
# Define the contract instance
MetadataStorage = w3.eth.contract(
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin']
)
def deploy_contract():
    tx = {
        'from': my_address,
        'gas': 105644,
        'gasPrice': w3.to_wei('1', 'gwei'),
        'nonce': w3.eth.get_transaction_count(my_address),
    }
    tx['data'] = MetadataStorage.constructor().build_transaction(tx)['data']
    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contract deployed at address: {tx_receipt.contractAddress}")
    return w3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'])

if __name__ == "__main__":
    if input == "file":
        ip = "ip3.jpg"
        op = "the_output_file3.7z"
        compress_file(ip, op)
        cid = upload_to_ipfs(op)
        contract_instance = deploy_contract()
        try:
            add_content(cid, "Description of the content", contract_instance)
            verify_content(cid, contract_instance)
        except Web3RPCError as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        try:
            file_content = retrieve_file_from_ipfs(cid)
            print("\n\n")
            decoded_string = file_content.decode('utf-8', errors='ignore')
            print(decoded_string)
        except Exception as e:
            print(e)
    else:
        ip_text = ""
        cid = add_claim(ip_text)
        contract_instance = deploy_contract()
        try:
            add_content(cid, "Description of the content", contract_instance)
            verify_content(cid, contract_instance)
        except Web3RPCError as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        try:
            file_content = retrieve_file_from_ipfs(cid)
            print("\n\n")
            decoded_string = file_content.decode('utf-8', errors='ignore')
            print(decoded_string)
        except Exception as e:
            print(e)