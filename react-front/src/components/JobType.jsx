import React, {Component} from 'react'
import ReactDOM from 'react-dom'


export default class JobType extends Component {
    onFull(e) {
        e.preventDefault();
        this.props.onChangeJobType("Full")
    }

    onIntern(e) {
        e.preventDefault();
        this.props.onChangeJobType("Internship")
    }


    render() {
        console.log('JobType')
        return(
            <div className="btn-group" data-toggle="buttons" >
                <label className="btn btn-default active" onClick={this.onFull.bind(this)} value="Full">
                    <input type="radio" name="inputWalls" id="inputWalls" value="Full"  />
                    Full Time 
                </label>
                <label className="btn btn-default" onClick={this.onIntern.bind(this)}>
                    <input type="radio" name="inputWalls" id="inputWalls" value="Internship"/>
                    Internship 
                </label>
            </div>
        )


    }


}


