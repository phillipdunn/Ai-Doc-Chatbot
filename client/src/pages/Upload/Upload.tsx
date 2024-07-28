import { Box, Button, Typography } from '@mui/material';
import React, { FC } from 'react';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';
import { toast } from 'react-toastify';

interface Props { }

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const Upload: FC<Props> = () => {

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', e.target.files[0]);
    fetch('upload_file', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        toast.success('File uploaded successfully');
      })
      .catch((error) => {
        toast.error('Error uploading file');
      });
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" sx={{ mt: 4 }}>Upload a file</Typography>

      <Button
        sx={{ mt: 2 }}
        component="label"
        role='button'
        variant="contained"
        tabIndex={-1}
        startIcon={<CloudUploadIcon />}
      >
        Upload file
        <VisuallyHiddenInput type="file" onChange={handleSubmit} />
      </Button>
    </Box>
  );
};

export default Upload;
