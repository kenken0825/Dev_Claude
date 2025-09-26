import { Request, Response, NextFunction } from 'express';
import Joi from 'joi';

const chatMessageSchema = Joi.object({
  message: Joi.string().min(1).max(1000).required(),
  sessionId: Joi.string().uuid().required(),
  userId: Joi.string().optional()
});

export const validateChatMessage = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const { error } = chatMessageSchema.validate(req.body);
  
  if (error) {
    return res.status(400).json({
      success: false,
      error: 'Invalid request data',
      details: error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message
      }))
    });
  }
  
  next();
};