import React from 'react'
import CircularProgress from '@material-ui/core/CircularProgress';
import { Typography } from '@material-ui/core';

function Loading(){
    return(
        <div className="loading">
            <div className="inner">
                <Typography variant="h3">Please Wait</Typography>
                <CircularProgress size="10%"  />
            </div>
        </div>
            
    )
}

export default Loading;