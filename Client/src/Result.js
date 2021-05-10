import React from 'react'
import $ from 'jquery';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
  root : {
    maxWidth: 345,
    textAlign: "center"
  },
  fake : {
    backgroundColor:"red",
    textAlign: "center"
  },
  real : {
    backgroundColor:"green",
    textAlign: "center"
  },
  media : {
    height: 140,
  },
});

function Result(props) {
    const frames = props.data.frames;
    const cropped = props.data.cropped;
    const faces = props.data.faces;
    const aligned = props.data;
    const fakes = props.data.fakeList;
    
    const classes = useStyles();  
  
    function scroll(direction){
        let far = $( '.image-container' ).width()/2*direction;
        let pos = $('.image-container').scrollLeft() + far;
        $('.image-container').animate( { scrollLeft: pos }, 1000)
    }
  
    return(
      <div className="main">
        <h1>Frames</h1>
        <div className="wrapper">
          <a className="prev" onClick={()=>scroll(-1)}>&#10094;</a>
          <div className="image-container">
            {frames.map((frame,key)=>{
                return(
                    <div key={key} className="image">
                      <Card className={classes.root}>
                        <CardActionArea>
                          <CardMedia>
                              <img src={frame} style={{objectFit: "contain",maxHeight: 400,maxWidth:400}} />
                          </CardMedia>  
                          <CardContent>
                          </CardContent>
                        </CardActionArea>
                      </Card>
                    </div>
                )
            })}
            
          </div>
          <a className="next" onClick={()=>scroll(1)}>&#10095;</a>
        </div>
        <h1>Cropped Faces</h1>
        <div className="wrapper">
          <a className="prev" onClick={()=>scroll(-1)}>&#10094;</a>
          <div className="image-container">
          {cropped.map((face,key)=>{
              return(
                <div key={key} className="image">
                  <Card className={classes.root}>
                    <CardActionArea>
                      <CardMedia>
                          <img src={face.file} style={{height: 400,width:400}} />
                      </CardMedia> 
                      <CardContent>
                      </CardContent>
                    </CardActionArea>
                  </Card>
                </div>
              )
          })}

          </div>
          <a className="next" onClick={()=>scroll(1)}>&#10095;</a>
        </div>
        <h1>Face Alignment and Model Prediction</h1>
        <div className="wrapper">
          <a className="prev" onClick={()=>scroll(-1)}>&#10094;</a>
          <div className="image-container">
          {faces.map((face,key)=>{
              if(face.prob>0.5)
                return(
                <div key={key} className="image">
                  <Card className={classes.root,classes.fake}>
                    <CardActionArea>
                      <CardMedia>
                      <img src={face.file} style={{height: 400,width:400}} />
                      </CardMedia>
                      <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                          Fake Probability : {face.prob}
                        </Typography>
                        <Typography gutterBottom variant="h5" component="h2">
                          Frame : {face.frame}
                        </Typography>
                      </CardContent>
                    </CardActionArea>
                  </Card>

                </div>
                )
              else
              return(
                <div>
                <div key={key} className="image">
                  <Card className={classes.root,classes.real}>
                    <CardActionArea>
                      <CardMedia>
                      <img src={face.file} style={{height: 400,width:400}} />
                      </CardMedia>
                      <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                          Fake Probability : {face.prob}
                        </Typography>
                        <Typography gutterBottom variant="h5" component="h2">
                          Frame : {face.frame}
                        </Typography>
                      </CardContent>
                    </CardActionArea>
                  </Card>
                </div>
                
                
                  </div>
              )
          })}
          </div>
          <a className="next" onClick={()=>scroll(1)}>&#10095;</a>
        </div>
        <h1>Fake faces</h1>
        <div className="wrapper">
          <a className="prev" onClick={()=>scroll(-1)}>&#10094;</a>
          <div className="image-container">
          {fakes.map((fake,key)=>{
              return(
                <div key={key} className="image">
                  <Card className={classes.root,classes.fake}>
                    <CardActionArea>
                      <CardMedia>
                      <img src={fake.file} style={{height: 400,width:400}} />
                      </CardMedia>
                      <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                          Fake Probability : {fake.prob}
                        </Typography>
                        <Typography gutterBottom variant="h5" component="h2">
                          Found in frame : {fake.frame}
                        </Typography>
                      </CardContent>
                    </CardActionArea>
                  </Card>
            </div>
              )
          })}
        
          </div>
          <a className="next" onClick={scroll(1)}>&#10095;</a>
        </div>
      </div>
      
    )
}
  
  export default Result;