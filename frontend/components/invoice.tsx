"use client";

import { useState, ChangeEvent } from "react";
import { CloudArrowUpIcon } from "@heroicons/react/24/outline";

export default function InvoiceUpload({ onFilesSelected }: InvoiceUploadProps) {
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;
        const fileArray = Array.from(files);
        setSelectedFiles(fileArray);
        onFilesSelected?.(fileArray);
    };

    return (
        <div className="max-w-md mx-auto">
            <label
                htmlFor="invoice-upload"
                className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-2xl p-8 cursor-pointer hover:border-gray-500 transition"
            >
                <CloudArrowUpIcon className="w-12 h-12 text-gray-400" />
                <span className="mt-2 text-gray-600">
                    Click to upload or drag and drop your invoices
                </span>
                <input
                    id="invoice-upload"
                    type="file"
                    multiple
                    accept="application/pdf,image/*"
                    onChange={handleFileChange}
                    className="hidden"
                />
            </label>

            {selectedFiles.length > 0 && (
                <ul className="mt-4 space-y-2">
                    {selectedFiles.map((file, index) => (
                        <li
                            key={index}
                            className="flex justify-between items-center bg-gray-100 p-2 rounded"
                        >
                            <span className="truncate">{file.name}</span>
                            <span className="text-sm text-gray-500">
                                {(file.size / 1024).toFixed(2)} KB
                            </span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
