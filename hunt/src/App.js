import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { ListView, ListViewItem, ListViewInfoItem, Row, Col, ListViewIcon } from 'patternfly-react';
import { VerticalNav, Dropdown, Icon, MenuItem } from 'patternfly-react';
import axios from 'axios';
import * as config from './config/Api.js';
import 'bootstrap3/dist/css/bootstrap.css'
import 'patternfly/dist/css/patternfly.css'
import 'patternfly/dist/css/patternfly-additions.css'
import 'patternfly-react/dist/css/patternfly-react.css'
import './App.css';

function onHomeClick() {
   ReactDOM.render(<RulesList />, document.getElementById('app-content'));
}

function onDashboardClick() {
   //ReactDOM.render(<RulesList />, document.getElementById('app-content'));
}

function onHistoryClick() {

}

class HuntApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sources: [], rulesets: []
    };
    this.displaySource = this.displaySource.bind(this);
    this.displayRuleset = this.displayRuleset.bind(this);
  }

    componentDidMount() {
      axios.all([
          axios.get(config.API_URL + config.SOURCE_PATH),
          axios.get(config.API_URL + config.RULESET_PATH),
	  ])
      .then(axios.spread((SrcRes, RulesetRes) => {
         this.setState({ rulesets: RulesetRes.data['results'], sources: SrcRes.data['results']});
      }))
    }

    displayRuleset(ruleset) {
    	ReactDOM.render(<Ruleset key={ruleset.pk} data={ruleset}/>, document.getElementById('app-content'));
    }
    
    displaySource(source) {
    	ReactDOM.render(<Source key={source.pk} data={source} />, document.getElementById('app-content'));
    }


    render() {
        return(
            <div className="layout-pf layout-pf-fixed faux-layout">
                <VerticalNav sessionKey="storybookItemsAsJsx" showBadges>
            	    <VerticalNav.Masthead title="Scirius">
						<VerticalNav.Brand iconImg="/static/rules/stamus.png" titleImg="brand-alt.svg" />
						<VerticalNav.IconBar>
							<UserNavInfo/>
						</VerticalNav.IconBar>
					</VerticalNav.Masthead>
		   <VerticalNav.Item
            	      title="Home"
            	      iconClass="fa fa-home"
            	      initialActive
            	      onClick={onHomeClick}
            	      className={null}
            	    />

            	    <VerticalNav.Item
            	      title="Dashboards"
            	      iconClass="fa fa-tachometer"
            	      onClick={onDashboardClick}
            	      className={null}
            	    >
            	        <VerticalNav.Badge count={42} />
            	    </VerticalNav.Item>
            	    <VerticalNav.Item title="IDS rules" iconClass="glyphicon glyphicon-eye-open">
            	        <VerticalNav.SecondaryItem title="Sources" >
                	    {this.state.sources.map(function(source) {
				    return(
	    		     <VerticalNav.TertiaryItem key={source.pk} title={source.name}  onClick={this.displaySource.bind(this, source)}  />
			     )
			     }, this)}
	    		     <VerticalNav.TertiaryItem title="Add Source" href="/rules/source/add" />
            	        </VerticalNav.SecondaryItem>
       			<VerticalNav.SecondaryItem title="Rulesets">
                	    {this.state.rulesets.map(function(ruleset) {
				    return(
	    		     <VerticalNav.TertiaryItem key={ruleset.pk} title={ruleset.name} onClick={this.displayRuleset.bind(this, ruleset)} />
			     )
			     }, this)}
	    		     <VerticalNav.TertiaryItem title="Add Ruleset" href="/rules/ruleset/add" >
        			<Icon type="pf" name="help" />
			     </VerticalNav.TertiaryItem>
            	        </VerticalNav.SecondaryItem>
       	             </VerticalNav.Item>
       		     <VerticalNav.Item
		      title="History"
		      iconClass="glyphicon glyphicon-list"
            	      onClick={onHistoryClick}
		     />
       		     <VerticalNav.Item 
		       title="Setup"
		       iconClass="glyphicon glyphicon-cog"
		       href="/appliances"
		     />
       		</VerticalNav>
       			<div className="container-fluid container-cards-pf container-pf-nav-pf-vertical">
       				<div className="row">
				    <div className="col-xs-12 col-sm-12 col-md-12" id="app-content" >
				    </div>
       				</div>
       			</div>
       		</div>
        )
    }
}


class UserNavInfo extends Component {
	render() {
		return(
			<React.Fragment>
    			<Dropdown componentClass="li" id="help">
      				<Dropdown.Toggle useAnchor className="nav-item-iconic">
        				<Icon type="pf" name="help" />
      				</Dropdown.Toggle>
      				<Dropdown.Menu>
        				<MenuItem>Help</MenuItem>
        				<MenuItem>About</MenuItem>
      				</Dropdown.Menu>
    			</Dropdown>
			    <Dropdown componentClass="li" id="time">
      				<Dropdown.Toggle useAnchor className="nav-item-iconic">
        				<Icon type="fa" name="clock-o" /> Last 24h
      				</Dropdown.Toggle>
      				<Dropdown.Menu>
        				<MenuItem>Last 1h</MenuItem>
        				<MenuItem>Last 6h</MenuItem>
    				</Dropdown.Menu>
			   </Dropdown>
			    <Dropdown componentClass="li" id="user">
      				<Dropdown.Toggle useAnchor className="nav-item-iconic">
        				<Icon type="pf" name="user" /> Eric Leblond
      				</Dropdown.Toggle>
      				<Dropdown.Menu>
        				<MenuItem>Preferences</MenuItem>
        				<MenuItem>Logout</MenuItem>
    				</Dropdown.Menu>
			   </Dropdown>
			</React.Fragment>
		)
	}
}

class RulesList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      rules: [], categories: []
    };
  }

  componentDidMount() {
      axios.all([
          axios.get(config.API_URL + config.RULE_PATH + "?ordering=-created&limit=10"),
          axios.get(config.API_URL + config.CATEGORY_PATH + "?limit=100"),
	  ])
      .then(axios.spread((RuleRes, CatRes) => {
	 var categories_array = CatRes.data['results'];
	 var categories = {};
	 for (var i = 0; i < categories_array.length; i++) {
	     var cat = categories_array[i];
	     categories[cat.pk] = cat;
	 }
         this.setState({ rules: RuleRes.data['results'], categories: categories});
      }))
  }
  
  render() {
    var state = this.state;
    return (
        <div className="RulesList">
	    <ListView>
            {this.state.rules.map(function(rule) {
                return(
                   <RuleInList key={rule.pk} data={rule} state={state}/>
                )
             })}
	    </ListView>
        </div>
    );
  }
}

class RuleInList extends Component {
  handleClick = () => {
    //this.setState({rule: {this.props.data}});
    const rdata = <Rule rule={this.props.data}/>
    ReactDOM.render(rdata, document.getElementById('app-content'));
  }
  render() {
    var category = this.props.state.categories[this.props.data.category];
    return (
	<ListViewItem
  actions={<button onClick={this.handleClick}>View</button>}
  leftContent={<ListViewIcon name="envelope" />}
  additionalInfo={[<ListViewInfoItem key="created"><p>Created: {this.props.data.created}</p></ListViewInfoItem>,
                   <ListViewInfoItem key="updated"><p>Updated: {this.props.data.updated}</p></ListViewInfoItem>,
                   <ListViewInfoItem key="category"><p>Category: {category.name}</p></ListViewInfoItem>
  ]}
  heading={this.props.data.sid}
  description={this.props.data.msg}
>
<Row>
<Col sm={11}>
{this.props.data.content}
</Col>
</Row>
</ListViewItem>
    )
  }
}


class Rule extends Component {
    render() {
        return (
            <h4>{this.props.rule.msg}</h4>
	)
    }
}

class Source extends Component {
    render() {
	var source = this.props.data;
        return (
            <h1>{source.name}</h1>
	)
    }
}

class Ruleset extends Component {
    render() {
	var ruleset = this.props.data;
        return (
            <h1>{ruleset.name}</h1>
	)
    }
}

export default HuntApp;
