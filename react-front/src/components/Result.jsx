import React, {Component} from 'react'
import ReactDOM from 'react-dom'


export default class Result extends Component {
    constructor(props) {
        super(props)
        this.state = {
            itemsPerPage: 5,
            curPage: 0
        }
    }


    onClick(arg){
        if (arg == 'next') {
            var page = Math.min(this.state.curPage+1, (this.props.positions.length / this.state.itemsPerPage) -1)
        } else if (arg == 'prev') {
            var page = Math.max(this.state.curPage-1, 0)
        } else {
            var page = arg;
        }
        console.log(page);
        this.setState({curPage : page})
    }

    render() {

        var pages = this.props.positions.length / this.state.itemsPerPage;
        this.state.pArray = []
        for (var i = 0; i < pages; i++) {
            this.state.pArray.push(i)
        }
        
        console.log(this.state.pArray)


        return(
            <div className="col-md-8">
                <br/>
                <div className="well well-lg">
                    <h3><span className="badge badge-default"> Recommendation Results</span></h3>
                    <ul className="list-group">
                        <a className="list-group-item">TITLE <p className = "pull-right">COMPANY</p></a>
                        {
                            this.props.positions.map((pos) => {
                                if ( ~~(pos.index/this.state.itemsPerPage) == this.state.curPage ) {
                                return <div key= {pos.index}>
                                        <a href={pos.url} target="_blank" className="list-group-item">{pos.title} <p className = "pull-right">{pos.company}</p></a>
                                    </div>
                                }
                            }) 
                        }
                    </ul>
                    <nav aria-label="Page navigation example">
                        <ul className="pagination">
                            <li className="page-item"><a className="page-link"  onClick={this.onClick.bind(this,"prev")} href="#">Previous</a></li>
                            {   
                                this.state.pArray.map((num)=> {
                                    return <li key = {num} className="page-item" onClick={this.onClick.bind(this,num)} ><a className="page-link" href="#">{num}</a></li>

                            })
                            
                            }
                            <li className="page-item"><a className="page-link" onClick={this.onClick.bind(this,"next")} href="#">Next</a></li>
                        </ul>
                    </nav>
                </div>
                
            </div>
        )


    }


}