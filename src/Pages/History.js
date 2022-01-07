import React from 'react';
import Header from '../Components/Header';
import Record from '../Components/Record';

export default class History extends React.Component {
    render() {
	return(
	    <>
                <Header redirect={true} link='/history'/>
                <Record/>
            </>
        )
    }
}

