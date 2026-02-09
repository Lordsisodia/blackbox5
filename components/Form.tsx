import React, { useState, useCallback, FormEvent, ChangeEvent } from 'react';

export interface FormField {
  name: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'textarea' | 'select';
  required?: boolean;
  placeholder?: string;
  options?: { value: string; label: string }[];
  validation?: (value: string) => string | null;
}

export interface FormProps {
  fields: FormField[];
  onSubmit: (data: Record<string, string>) => void | Promise<void>;
  submitLabel?: string;
  loading?: boolean;
  className?: string;
}

export function Form({
  fields,
  onSubmit,
  submitLabel = 'Submit',
  loading = false,
  className = '',
}: FormProps) {
  const [values, setValues] = useState<Record<string, string>>(() =>
    fields.reduce((acc, field) => ({ ...acc, [field.name]: '' }), {})
  );
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validateField = useCallback(
    (field: FormField, value: string): string | null => {
      if (field.required && !value.trim()) {
        return `${field.label} is required`;
      }
      if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          return 'Please enter a valid email address';
        }
      }
      if (field.validation) {
        return field.validation(value);
      }
      return null;
    },
    []
  );

  const handleChange = useCallback(
    (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const { name, value } = e.target;
      setValues((prev) => ({ ...prev, [name]: value }));

      const field = fields.find((f) => f.name === name);
      if (field && touched[name]) {
        const error = validateField(field, value);
        setErrors((prev) => ({ ...prev, [name]: error || '' }));
      }
    },
    [fields, touched, validateField]
  );

  const handleBlur = useCallback(
    (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const { name, value } = e.target;
      setTouched((prev) => ({ ...prev, [name]: true }));

      const field = fields.find((f) => f.name === name);
      if (field) {
        const error = validateField(field, value);
        setErrors((prev) => ({ ...prev, [name]: error || '' }));
      }
    },
    [fields, validateField]
  );

  const handleSubmit = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();

      const newErrors: Record<string, string> = {};
      let hasErrors = false;

      fields.forEach((field) => {
        const error = validateField(field, values[field.name]);
        if (error) {
          newErrors[field.name] = error;
          hasErrors = true;
        }
      });

      setErrors(newErrors);
      setTouched(fields.reduce((acc, f) => ({ ...acc, [f.name]: true }), {}));

      if (!hasErrors) {
        await onSubmit(values);
      }
    },
    [fields, onSubmit, values, validateField]
  );

  const renderField = (field: FormField) => {
    const baseInputClasses =
      'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors';
    const errorClasses = errors[field.name]
      ? 'border-red-500 focus:ring-red-500'
      : 'border-gray-300';

    const inputProps = {
      id: field.name,
      name: field.name,
      value: values[field.name],
      onChange: handleChange,
      onBlur: handleBlur,
      placeholder: field.placeholder,
      disabled: loading,
      className: `${baseInputClasses} ${errorClasses}`,
    };

    switch (field.type) {
      case 'textarea':
        return <textarea {...inputProps} rows={4} />;
      case 'select':
        return (
          <select {...inputProps}>
            <option value="">Select {field.label}</option>
            {field.options?.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        );
      default:
        return <input type={field.type || 'text'} {...inputProps} />;
    }
  };

  return (
    <form onSubmit={handleSubmit} className={`space-y-4 ${className}`}>
      {fields.map((field) => (
        <div key={field.name} className="space-y-1">
          <label
            htmlFor={field.name}
            className="block text-sm font-medium text-gray-700"
          >
            {field.label}
            {field.required && <span className="text-red-500 ml-1">*</span>}
          </label>
          {renderField(field)}
          {errors[field.name] && (
            <p className="text-sm text-red-600">{errors[field.name]}</p>
          )}
        </div>
      ))}
      <button
        type="submit"
        disabled={loading}
        className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700
                   disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors
                   font-medium"
      >
        {loading ? 'Submitting...' : submitLabel}
      </button>
    </form>
  );
}

export default Form;
