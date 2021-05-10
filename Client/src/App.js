import './index.css';
import React from 'react';
import Loading from './Loading';
import Result from './Result';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import Modal from 'react-modal'
import InfoIcon from '@material-ui/icons/Info';

const outerModal = { 
  modal: {
      backgroundColor: "green",
  },
  overlay: {
      backgroundColor: "grey",
  }, 
  content: {
      width:'40%',
      height: '70%',
      alignContent:'center',
      marginLeft: "28%",
      marginTop: "3%",
      overflow: 'auto',
      backgroundColor: "white",
      border: 'none',
      overflow: 'hidden'
  }
}

function App() {
  const [fileName,setFileName] = React.useState("");
  const [image,setImage] = React.useState("");
  const [data,setData] = React.useState({});
  const [isLoading,setIsLoading] = React.useState(false)
  const [showResult,setShowResult] = React.useState(false);
  const [isInvalid,setIsInvalid] = React.useState(false)
  const [isReal,setIsReal] = React.useState(true)
  const [showOp,setShowOp] = React.useState(false);
  const [showModal, setShowModal] = React.useState(false);

  function getExtension(filename) {
    var parts = filename.split('.');
    return parts[parts.length - 1];
  }

  function onSubmit(){
    setIsLoading(true);
    const data = new FormData() 
    const extention = getExtension(fileName);
    if(extention.length == 0){
      setIsInvalid(true);
      setShowOp(true);
      setIsLoading(false)
      return;
    }
    setImage(image);
    setFileName(fileName);
    data.append('imagePath', image, fileName);
    if(extention == "JPG" || extention == "PNG"){
      let url = "http://127.0.0.1:8000/predict-image/";

        axios.post(url, data, {  
        })
        .then(res => {
            var ans = res.data.res
            if(ans.faces.length==0)
              setIsInvalid(true)
            else
              setIsInvalid(false)
            if(ans.fakeList.length>0)
              setIsReal(false)
            else
              setIsReal(true)
            setData(ans);
            setShowOp(true);
            setIsLoading(false);
        })
      }
      else if(getExtension(fileName)=="mp4"){
        let url = "http://127.0.0.1:8000/predict-video/";
  
          axios.post(url, data, {  
          })
          .then(res => {
            var ans = res.data.res
            if(ans.faces.length==0)
              setIsInvalid(true)
            else
              setIsInvalid(false)
            if(ans.fakeList.length>0)
              setIsReal(false)
            else
              setIsReal(true)
            setData(ans);
            setShowOp(true);
            setIsLoading(false);
          })
        }
  }
  function onFileChange(e){
    setImage(e.target.files[0])
    setFileName(e.target.files[0].name)
  }
  if(showModal)
    return(
      <Modal scrollable={true} ariaHideApp={false} isOpen={showModal} onRequestClose={()=>setShowModal(false) } style={outerModal} >
          <div >
                <h1 style={{textAlign: 'center'}}>Our Formula for DeepFake Detection</h1>
                <img width="100%" height="100%" src="archi.PNG" />
                <ul>
                  <li><Typography>The entire system is made up of several modules bundled together to give the best possible results.</Typography></li>
                  <li><Typography  display="inline">Starting from the face detection, we have used the best and the fastest model by using </Typography><Typography display="inline" style={{color:"red"}}>MTCNN</Typography><Typography display="inline">. It is now possible to detect not only frontal face but non-frontal faces could also be detected using this model.</Typography></li>
                  <li><Typography>Face alignment is an important process to reduce irregularities so that our model is consistent and can give result in the shortest possible time.</Typography></li>
                  <li><Typography display="inline">For detection, we have trained our</Typography><Typography display="inline" style={{color:"red"}}> ML model (XceptionNet and DenseNet) </Typography><Typography display="inline">on huge collection of real and fake images to make our model robust and accurate.</Typography></li>
                </ul>
          </div>
          
        </Modal>
    )
  else if(showResult)
    return(
      <div style={{marginTop:"3%"}}>
        <Result data={data} />
      </div>
    )
  else if(isLoading)
    return(
      <div className="app">
        <div className="box" style={{height:"30%"}}>
        <Loading />
        </div>
      </div>
    )
  else
  return (
    <div className="app">
        <div className="box" style={{boxShadow:"20%"}}>
          <Typography variant="h3">DeepFake Detection <InfoIcon style={{cursor: "pointer"}} onClick={()=> setShowModal(true) }/></Typography>
              <Box  mt={2}>
              <input
                onChange = {onFileChange}
                style={{ display: 'none'}}
                id="image"
                name="videoPath"
                type="file"
              />
              <label htmlFor="image">
                <Button
                  style={{width: "80%",backgroundColor:"rgb(223, 217, 217)"}}
                  variant="outlined"
                  color="default"
                  component="span"
                  size="large"
                  fullWidth
                >
                  Upload your Image / Video
                </Button>
                <Typography
                  variant="caption"
                  display="block"
                  style={{padding: "1", fontStyle: 'italic', color: 'black',fontSize:"20px" }}
                >
                {fileName}
                </Typography>
              </label>
            </Box>
            <Button onClick={onSubmit} variant="contained" style={{marginTop:"4%"}} >Submit</Button>
            {isInvalid && showOp ? (
              <div style={{textAlign:"left"}}>
                <ul style={{marginLeft:"10%"}}>
                <Typography color="secondary" variant="h5">INVALID INPUT</Typography>
                  <li><Typography variant="h6">Input should contain atleast one face</Typography></li>
                  <li><Typography variant="h6" >Size of video should be less than 20MB</Typography></li>
                  <li><Typography variant="h6" >Video should be less than 10 seconds</Typography></li>
                </ul>
              </div>
            ): (
              <div />
            )}
            {isReal && showOp && !isInvalid? (
              <>
                <h2 style={{display:"inline"}}>RESULT :</h2><Typography style={{display:"inline",color:"green"}} color="primary" variant="h5"> NO DEEPFAKE DETECTED</Typography>
                <Button onClick={()=>{setShowResult(true)}} variant="contained">View Frame by Frame Analysis</Button>
              </>
            ) : ( showOp && !isInvalid ? (
              <>
                <h2 style={{display:"inline"}}>RESULT :</h2><Typography style={{display:"inline"}} color="error" variant="h5"> DEEPFAKE DETECTED</Typography>
                <Button onClick={()=>{setShowResult(true)}} variant="contained">View Frame by Frame Analysis</Button>
              </>
            ) : <div />
              
            )}
          </div>
      </div>
      
  );
}

export default App;
