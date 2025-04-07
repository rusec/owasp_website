import express from "express";

const app = express();
const PORT = process.env.PORT || 5000;
const ORIGIN = process.env.ORIGIN || "http://localhost:5000";
const cors = require("cors");

app.use(
    cors({
        origin: ORIGIN,
        methods: ["GET", "POST"],
        credentials: true,
    })
);
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
