import axios, { AxiosResponse } from 'axios';

export default class Substation {
    // Properties
    id: number;
    leftNeighbor: Substation | null;
    rightNeighbor: Substation | null;
    currentLoad: number = 0;
    predictedLoad: number = 0;

    
    // Constructor
    constructor(id: number) {
        this.id = id;
        this.leftNeighbor = null;
        this.rightNeighbor = null;
    }

    // Methods for Server Calls
    async makeHttpGetRequest(url: string): Promise<AxiosResponse> {
        try {
            const response = await axios.get(url);
            return response;
        } catch (error) {
            throw error;
        }
    }

    async makeHttpPostRequest(url: string, data: any): Promise<AxiosResponse> {
        try {
            const response = await axios.post(url, data);
            return response;
        } catch (error) {
            throw error;
        }
    }

    getPredicationData = async ({
        collection_name,
        year,
        month,
        day,
        temperature
    }:{
        collection_name: string,
        year: number,
        month: number,
        day: number,
        temperature: number
    }): Promise<string[]> => {
        let user_data = {
            "collection_name": collection_name,
            "year": year,
            "month": month,
            "day": day,
            "temperature": temperature
        }
        const response = await this.makeHttpPostRequest("http://127.0.0.1:5000/predict", user_data);

        if (response.status != 200) {
            console.log("Error: Cannot get the prediction data")
            return []
        }

        let prediction_data: string[] = response.data

        return prediction_data

    }

    // Methods For Neighbors
    getLeftNeighbor(): Substation | null {
        return this.leftNeighbor;
    }
    
    setLeftNeighbor(substation: Substation): void {
        this.leftNeighbor = substation;
    }

    getRightNeighbor(): Substation | null {
        return this.rightNeighbor;
    }

    setRightNeighbor(substation: Substation): void {
        this.rightNeighbor = substation;
    }

    // Methods For Load

    getCurrentLoad(): number {
        return this.currentLoad;
    }

    setCurrentLoad(load: number): void {
        this.currentLoad = load;
    }

    getPredictedLoad(): number {
        return this.predictedLoad;
    }

    setPredictedLoad(load: number): void {
        this.predictedLoad = load;
    }

    // Substation ID

    getID(): number {
        return this.id;
    }

    // Methods For Deciding Load Necessities

    hasExcessLoad(): boolean {
        return this.currentLoad > this.predictedLoad;
    }

    getExcessLoad(): number {
        return this.currentLoad - this.predictedLoad;
    }

    hasShortage(): boolean {
        return this.currentLoad < this.predictedLoad;
    }

    getShortage(): number {
        return this.predictedLoad - this.currentLoad;
    }

    // Methods For Load Transfer

    // transferLoadTo(substation: Substation): void {
    //     let loadToTransfer = this.getExcessLoad();
    //     // TODO - Add logic to add blockchain transaction here
    //     this.currentLoad -= loadToTransfer;
    //     substation.currentLoad += loadToTransfer;
    // }

    async transferLoadFrom(substation: Substation): Promise<void | string> {
        let loadToTransfer = substation.getShortage();

		let response = await this.makeHttpGetRequest('http://127.0.0.1:5000/blockchain/last')
		
		let index = 0
		let previous_hash = "0"  // Use the Genesis block's  hash when the blockchain is empty

		if (response.status != 200) {
			console.log("Error: Cannot get the last block")
			index = 0
			previous_hash = "0"  // Use the Genesis block's hash when the blockchain is empty
		}

		let last_block = response.data

		previous_hash = last_block['previous_hash']
		index = last_block['index'] + 1

		const currentDate = new Date();

		let data_to_upload = {
			'index': index,
			'previous_hash': previous_hash,
			'timestamp': currentDate.getTime(),
			'data': {
				's_address': substation.id.toString(),
				'r_address': this.id.toString(),
				'amount': loadToTransfer.toString(),
				'price': 'Substation to Substation',
			}
		}

		response = await this.makeHttpPostRequest("http://localhost:5000/blockchain/transaction", data_to_upload)

		if (response.status != 200) {
			console.log("Error: Cannot upload the transaction")
			return "Error: Cannot upload the transaction"
		}

		this.currentLoad += loadToTransfer;
		substation.currentLoad -= loadToTransfer;
	}

    async lookForLoadTransfer(): Promise<void> {
        if (this.hasShortage()) {
            // Start by looking left
            let currentSubstation: Substation | null = this.leftNeighbor;
            
            // Continue looking left until there are no more neighbors or until you find a neighbor with excess load
            while (currentSubstation && currentSubstation.hasExcessLoad() && this.hasShortage()) {
                await this.transferLoadFrom(currentSubstation);
                currentSubstation = currentSubstation.leftNeighbor;
            }
    
            // If there are no more neighbors with excess load on the left, look to the right
            currentSubstation = this.rightNeighbor;
            
            // Continue looking right until there are no more neighbors or until you find a neighbor with excess load
            while (currentSubstation && currentSubstation.hasExcessLoad() && this.hasShortage()) {
                await this.transferLoadFrom(currentSubstation);
                currentSubstation = currentSubstation.rightNeighbor;
            }

            while (this.hasShortage()) {
                console.log("There is still a shortage");
                const response = await this.makeHttpGetRequest("http://localhost:5000/all_contracts")

				let contracts = response.data

				contracts.forEach(async (contract: any) => {
					if (contract['executed'] == false) {
						let address = contract['address']

						const execute_response = await this.makeHttpGetRequest("http://localhost:5000/execute_contract/" + address)

						if (execute_response.status != 200) {
							console.log("Error: Cannot execute the contract")
							return "Error: Cannot execute the contract"
						}

						this.currentLoad += contract['data']['amount']

						let sender_address = contract['owner']
					}
					if (!this.hasShortage()) {
						return
					}
				})

				// TODO - Add logic to add generator transaction here
            }
        }
    }
}