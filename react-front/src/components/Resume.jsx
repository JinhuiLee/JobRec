import React, {Component} from 'react'
import ReactDOM from 'react-dom'


export default class Resume extends Component {

    onDemo(e) {
        e.preventDefault();
        this.refs.resumeInfo.value = "JOHN T. PARSONS \n \
        Sometown, GA 30082 \n \
        (555) 555-5555 | jp@somedomain.com | LinkedIn URL \n \
        Director of Software Development \
        Engineering robust, user-focused solutions driving breakthrough efficiency and bottom-line results \
        Dynamic leader of software development teams offering 11 years of experience managing multimillion-dollar, mission-critical projects. \
        Skilled in all phases of the software development lifecycle; expert in translating business requirements into technical solutions; and fanatical about quality, usability, security and scalability. \
        Application Development "
        this.onSubmitResume(e)
    }

    onSubmitResume(e) {
        e.preventDefault();
        let resumeInfo = this.refs.resumeInfo.value
        console.log(
            "debug"
        )
        if (resumeInfo.length > 50)
            this.props.getRecPosition(resumeInfo)
    }


    onClear(e) {
        e.preventDefault();
        this.refs.resumeInfo.value = ''
        
    }
    

    render() {
        console.log('hello')
        return(
            <div className="col-md-4">
                <div className="form-group">
                        <label >Copy your resume into here</label>
                        <textarea className="form-control" ref="resumeInfo" rows="20" id="comment"></textarea>
                     <br/>
                    <div className="col-md-12">
                        <button type="button" onClick={this.onDemo.bind(this)} className="btn btn-primary">Demo</button>
                        <button type="button" onClick={this.onSubmitResume.bind(this)} className="btn btn-success ">Submit</button>
                        <button type="button" onClick={this.onClear.bind(this)} className="btn btn-info">Clear</button>
                    </div>
                </div>
            </div>
        )


    }


}