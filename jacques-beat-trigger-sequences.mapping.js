

/* ********** GENERAL SCRIPTING **********************

		This templates shows what you can do in this is module script
		All the code outside functions will be executed each time this script is loaded, meaning at file load, when hitting the "reload" button or when saving this file
*/


// You can add custom parameters to use in your script here, they will be replaced each time this script is saved
var currentTrackName = script.addStringParameter("Current Track Name","Current track name", "cool");	//This will add a string parameter (text field), default value is "cool"
// var mappingJsonFile = script.addFileParameter("Mapping JSON", "Mapping JSON file");					//Adds a file parameter to browse for a file. Can have a third argument "directoryMode" 										
var sequenceIndex = script.addIntParameter("Sequence Index","Sequence Index based on track name", 0, 0, 100);	

//you can also declare custom internal variable
//var myValue = 5;

/*
 The init() function will allow you to init everything you want after the script has been checked and loaded
 WARNING it also means that if you change values of your parameters by hand and set their values inside the init() function, they will be reset to this value each time the script is reloaded !
*/
function init()
{
	//myFloatParam.set(5); //The .set() function set the parameter to this value.
	//myColorParam.set([1,.5,1,1]);	//for a color parameter, you need to pass an array with 3 (RGB) or 4 (RGBA) values.
	//myP2DParam.set([1.5,-5]); // for a Point2D parameter, you need to pass 2 values (XY)
	//myP3DParam.set([1.5,2,-3]); // for a Point3D parameter, you need to pass 3 values (XYZ)
}

/*
 This function will be called each time a parameter of your script has changed
*/
function scriptParameterChanged(param)
{
	//You can use the script.log() function to show an information inside the logger panel. To be able to actuallt see it in the logger panel, you will have to turn on "Log" on this script.
	script.log("Parameter changed : "+param.name); //All parameters have "name" property
	if(param.is(myTrigger)) 
	{
		script.log("Trigger !"); //You can check if two variables are the reference to the same parameter or object with the method .is()
		//Here we can for example show a "Ok cancel" box. The result will be called in the messageBoxCallback function below
		//util.showOkCancelBox("myBoxId", "Super warning!", "This is a warning for you", "warning", "Got it","Naaah");
	}
	else if(param.is(myEnumParam))
	{
		script.log("Key = "+param.getKey()+", data = "+param.get()); //The enum parameter has a special function getKey() to get the key associated to the option. .get() will give you the data associated
	}
	else
	{
		script.log("Value is "+param.get()); //All parameters have a get() method that will return their value
	} 
}

/*
 This function, if you declare it, will launch a timer at 50hz, calling this method on each tick
*/
/*
function update(deltaTime)
{
	script.log("Update : "+util.getTime()+", delta = "+deltaTime); //deltaTime is the time between now and last update() call, util.getTime() will give you a timestamp relative to either the launch time of the software, or the start of the computer.
}
*/

/*
 This function, if you declare it, will be called when after a user has made a choice from a okCancel box or YesNoCancel box that you launched from this script 
*/
/*
function messageBoxCallback(id, result)
{
	script.log("Message box callback : "+id+" > "+result); //deltaTime is the time between now and last update() call, util.getTime() will give you a timestamp relative to either the launch time of the software, or the start of the computer.
}
*/

/* ********** FILTER SPECIFIC SCRIPTING **********************

	The "local" variable refers to the object containing the scripts. In this case, the local variable refers to the filter.
	It means that you can access any control inside  this filter by accessing it through its address.
*/

/*
 This function will be called each time the filter is processed, and expects a return value.
 This function only exists because the script is in a filter
 The "inputs" argument is an array of all the parameters that are being filtered. Each element can be either a single value or an array of values itself (if it's a Color or Point 2D/3D for instance)

 The minValues and max Values are arrays of the same size as inputs, containing the value range of the input if applicable 

 If this filter is inside a multiplexed mapping, multiplexIndex is the current index of the multiplex list

 The result must be an array of the same size as the inputValues

*/

var trackNames = ["Concrete Angel", "Transcendence"];

function getSequenceIndex(trackName)
{
	var key;
	for(var i = 0; i < trackNames.length; i++) {
		key = trackNames[i];
		script.log("Checking track name: "+trackName+", sequence name: "+key);
		script.log("index of string: "+trackName.indexOf(key));
		if (trackName.indexOf(key) != -1) {
			script.log("Sequence found for track name: "+trackName+", sequence name: "+key);
			// TODO can introduce remapper here
			return i;
		}
	}

	script.log("No sequence found for track name: "+trackName);
	return 0;
};

function filter(inputs, minValues, maxValues, multiplexIndex)
{
	var result = [];
	for(var i = 0; i < inputs.length; i++)
	{
		result[i] = inputs[i]; 
	}

	var mappedSequenceIndex = getSequenceIndex(currentTrackName.get());
	script.log("Mapped sequence index: "+mappedSequenceIndex);
	sequenceIndex.set(mappedSequenceIndex);

	root.states.state.processors.action.consequencesTRUE.consequence1.command.sequenceIndex.set(mappedSequenceIndex);
	root.states.state.processors.action.trigger.trigger();

	return result;
}
