import React from 'react';
import { create, ReactTestRenderer } from 'react-test-renderer';
import Message from './Message';


describe('Message', () => {
    let component: ReactTestRenderer;

    beforeEach(() => {
        component = create(<Message key={1} message='this messgae' position='left_bubble' />);
    });

    it('should render', () => {
        expect(component).toBeTruthy();
    });

    it('should render the message', () => {
        expect(component.toJSON()).toMatchSnapshot();
    });
});
