import React, {Component} from 'react'
import ReactDOM from 'react-dom'
import JobType from './components/JobType.jsx'
import Resume from './components/Resume.jsx'
import Result from './components/Result.jsx'
export default class App extends Component {

    constructor(props) {
        super(props)
        this.state = {
            positions : [],
            jobType : "Full"
        }
    }

    onChangeJobType(type) {
        this.setState({jobType: type})
    }

    getRecPosition(doc) {
        // console.log(doc)
        if (this.state.jobType == "Full") {
            var url = 'http://localhost:5000/api/recommend'
        } else {
            var url = 'http://localhost:5000/api/recommendIntern'
        }
        $.ajax({
            url: url,
            dataType: 'json',
            type: "POST",
            data: {'data':doc},
            success: function(data) {
                console.log(data)
                this.setState({positions : data})
            }.bind(this),
            error: function(xhr, status, err) {
                
            }.bind(this)

        })
    }


    render() {
        console.log('hello')
        return  <div>
            <JobType jobType = {this.state.jobType} onChangeJobType = {this.onChangeJobType.bind(this)}/>
            <div className = "row">
                <Resume getRecPosition = {this.getRecPosition.bind(this)}/>
                <Result positions = {this.state.positions}/>
            </div>
        </div>
            
           
           
        
    }


}