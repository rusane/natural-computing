"use strict"

// Adhesion constants
const CELL_VOLUME = 200;            // cell volume
const J_CELL_BACKGROUND = 20;       // cell-matrix adhesion  
const J_CELL_CELL = 0;              // cell-cell adhesion
const J_CELL_OBSTACLE = 0;          // cell-obstacle adhesion 
const J_OBSTACLE_BACKGROUND = 20;   // obstacle-matrix adhesion
const J_OBSTACLE_OBSTACLE = 0;      // obstacle-obstacle adhesion

// Cell parameters
let cell = {
  LAMBDA_V: 50,
  V: CELL_VOLUME,
  LAMBDA_P: 2,
  P: 180,
  LAMBDA_ACT: 200,
  MAX_ACT: 80
};

// Round obstacle parameters
let obstacle = {
  LAMBDA_V: 1000,
  V: 0.5 * CELL_VOLUME,
  LAMBDA_P: 200,
  // compute perimeter of a circle given the volume
  get P() {
    return 2 * Math.PI * Math.sqrt(this.V / Math.PI);
  },
  LAMBDA_ACT: 0,
  MAX_ACT: 0
};

let config = {
  // Grid settings
  ndim: 2,
  field_size: [200, 200],

  // CPM parameters and configuration
  conf: {
    seed: 42, // Seed for random number generation
    T: 20,    // CPM temperature

    // Constraint parameters. 
    // Mostly these have the format of an array in which each element specifies the
    // parameter value for one of the cellkinds on the grid.
    // First value is always cellkind 0 (the background) and is often not used.

    // Adhesion parameters:
    J: [
      [0, J_CELL_BACKGROUND, J_OBSTACLE_BACKGROUND], // Background
      [J_CELL_BACKGROUND, J_CELL_CELL, J_CELL_OBSTACLE], // migrating cell 
      [J_OBSTACLE_BACKGROUND, J_CELL_OBSTACLE, J_OBSTACLE_OBSTACLE] // Obstacle cell
    ],

    // VolumeConstraint parameters
    LAMBDA_V: [0, cell.LAMBDA_V, obstacle.LAMBDA_V],        // VolumeConstraint importance per cellkind
    V: [0, cell.V, obstacle.V],                             // Target volume of each cellkind

    // PerimeterConstraint parameters
    LAMBDA_P: [0, cell.LAMBDA_P, obstacle.LAMBDA_P],        // PerimeterConstraint importance per cellkind
    P: [0, cell.P, obstacle.P],                             // Target perimeter of each cellkind

    // ActivityConstraint parameters
    LAMBDA_ACT: [0, cell.LAMBDA_ACT, obstacle.LAMBDA_ACT],  // ActivityConstraint importance per cellkind
    MAX_ACT: [0, cell.MAX_ACT, obstacle.MAX_ACT],				    // Activity memory duration per cellkind
    ACT_MEAN: "geometric"                                   // Is neighborhood activity computed as a "geometric" or "arithmetic" mean?
  },

  // Simulation setup and configuration
  simsettings: {
    // Cells on the grid
    NRCELLS: [20, 10],                // Number of cells to seed for all non-background cellkinds.

    RUNTIME: 500,                     // Only used in node

    CANVASCOLOR: "eaecef",
    CELLCOLOR: ["000000","ffffff","cccccc","cccccc"],
    ACTCOLOR: [true, false],			    // Should pixel activity values be displayed?
    SHOWBORDERS: [false, true],       // Should cellborders be displayed?

    zoom: 2,                          // zoom in on canvas with this factor

    IMGFRAMERATE: 1
  }
};

// Initialize simulation
let sim;

function initialize() {
  let custommethods = {
    initializeGrid : initializeGrid
  }
  sim = new CPM.Simulation(config, custommethods);
  setAddCell();
  setAddCells10();
  setAddCells100();
  setRemove();
  setRunToggler();
  step();
}

/* The following custom methods will be added to the simulation object*/
function initializeGrid(){

	// add the initializer if not already there 
	if( !this.helpClasses["gm"] ){ this.addGridManipulator() }

	// Seed obstacle cells
    createObstacles()
}

function createObstacles() {
    // Seed obstacle cell layer 
    let step = 48
    for (var i = 1; i < sim.C.extents[0]; i += step) {
        for (var j = 1; j < sim.C.extents[1]; j += step) {
            sim.gm.seedCellAt(2, [i, j])
        }
    }
}

function step() {
  sim.step();
  requestAnimationFrame(step);
}

function setRunToggler() {
  let runButton = document.getElementById("toggle-run");
  runButton.addEventListener("click", () => {
    sim.toggleRunning();
    if (runButton.innerHTML.includes("stop")) {
      runButton.innerHTML = "start ▶";
    } else {
      runButton.innerHTML = "stop ⏹";
    }
  })
}

// Function to add one cell when button is clicked
function setAddCell() {
  let add1Button = document.getElementById("add-cell");
  add1Button.addEventListener("click", () => {
    // Seed 1 cell
	  seedCell( 1 )
  })
}

// Function to add ten cells when button is clicked
function setAddCells10() {
  let add10Button = document.getElementById("add-cell-10");
  add10Button.addEventListener("click", () => {
    // Seed 10 cell
	  seedCells( 10 )
  })
}

// Function to add hundred cells when button is clicked
function setAddCells100() {
  let add100Button = document.getElementById("add-cell-100");
  add100Button.addEventListener("click", () => {
    // Seed 100 cell
	  seedCells( 100 )
  })
}

// Function to add hundred cells when button is clicked
function setRemove() {
  let removeButton = document.getElementById("remove");
  removeButton.addEventListener("click", () => {
    // Remove all cells
    killAllCells()
    // re-seed obstacles
    createObstacles()
  })
}

function seedCell( k ){
	sim.gm.seedCell(k)
}

function seedCells( ncells ){
	for( let i = 0; i < ncells; i++ ){
		seedCell( 1 )
  }
}

function killAllCells(){
	let cells = Object.keys( sim.C.getStat( CPM.PixelsByCell ) )
	if( cells.length == 0 ) return
	for( let cp of sim.C.cellPixels() ){
		sim.C.setpix( cp[0], 0 )
	}
}