import React from 'react';
import { create } from 'react-test-renderer'; // Import the 'create' function
import Upload from './Upload';

describe('Upload', () => {
    it('should render without crashing', () => {
        const component = create(<Upload />);
        expect(component).toBeTruthy();
    });
});
