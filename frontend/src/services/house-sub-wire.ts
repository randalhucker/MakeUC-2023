class HouseSubstationWire {
    values: [number[], number[], number[]];
    constructor() {
        this.values = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    }

    set(substationID: number, houseID: number, value: number) {
        this.values[substationID][houseID] = value;
    }
    get(substationID: number) {
        return this.values[substationID];
    }
};

export default new HouseSubstationWire();