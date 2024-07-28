import React from 'react';
import { create } from 'react-test-renderer'; // Import the 'create' function instead of 'ReactTestRenderer'
import Chat from './Chat';

describe('Chat', () => {
    it('should render without crashing', () => {
        const component = create(<Chat />);
        expect(component).toBeTruthy();
    });
});
