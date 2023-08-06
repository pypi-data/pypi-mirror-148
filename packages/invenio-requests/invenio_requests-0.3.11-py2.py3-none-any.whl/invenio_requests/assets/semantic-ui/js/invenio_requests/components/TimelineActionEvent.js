// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import { Feed } from "semantic-ui-react";
import { TimelineEventBody } from "./TimelineEventBody";
import { Image } from "react-invenio-forms";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import RequestsFeed from "./RequestsFeed";

class TimelineActionEvent extends Component {
  render() {
    const { event, iconName, iconColor, userAction } = this.props;

    return (
      <Overridable
        id="TimelineActionEvent.layout"
        event={event}
        iconName={iconName}
        iconColor={iconColor}
        userAction={userAction}
      >
        <RequestsFeed.Item>
          <RequestsFeed.Content isEvent={true}>
            <RequestsFeed.Icon name={iconName} size="large" color={iconColor}/>
            <RequestsFeed.Event isActionEvent={true}>
              <Feed.Label>
                {userAction && (
                  <Image
                    src="/static/images/square-placeholder.png"
                    as={Image}
                    rounded
                    avatar
                  />
                )}
              </Feed.Label>
              <Feed.Content>
                <div className="flex">
                  {userAction && (
                    <b className="mr-5">{event.created_by.name}</b>
                  )}
                  <TimelineEventBody
                    content={event?.payload?.content}
                    format={event?.payload?.format}
                  />
                </div>
              </Feed.Content>
            </RequestsFeed.Event>
          </RequestsFeed.Content>
        </RequestsFeed.Item>
      </Overridable>
    );
  }
}

TimelineActionEvent.propTypes = {
  event: PropTypes.object.isRequired,
  iconName: PropTypes.string.isRequired,
  iconColor: PropTypes.string,
  userAction: PropTypes.bool,
};

TimelineActionEvent.defaultProps = {
  iconColor: "grey",
  userAction: true,
};

export default Overridable.component(
  "TimelineActionEvent",
  TimelineActionEvent
);
